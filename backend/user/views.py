import time
from datetime import datetime

from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import User
from .serializers import UserSerializer
from .utils import decrypt
from django.conf import settings
from backend.redis_client import redis_client


"""
@last-edit-date 2026-04-23
@author tyd
@desc 用户登录接口

"""
@api_view(['POST'])
@permission_classes([])
def login(request):
    username  = request.data.get("userName", "").strip() # 获取用户名
    password = request.data.get("password", "").strip()  # 获取密码（加过密的）
    decrypt_password = decrypt(password, settings.CRYPTOJS_KEY) # 解密
    user = authenticate(username=username, password=decrypt_password) # 验证是否正确
    if not user:
        return Response({
            "code": 401,
            "message": "用户名或密码错误"
        }, status=status.HTTP_401_UNAUTHORIZED)

    if (user.status == 'inactive'):
        return Response({
            "code": 403,
            "message": "用户已被禁用，请联系管理员"
        }, status=status.HTTP_403_FORBIDDEN)
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    serializer = UserSerializer(user)

    return Response({
        "code": 200,
        "data": {
            "user": serializer.data,
            "accessToken": access_token,
            "refreshToken": str(refresh)
        },
        "currentTimeMillis": int(time.time() * 1000)
    }, status=status.HTTP_200_OK)



"""
@last-edit-date 2026-04-23
@author tyd
@desc 注册用户接口

"""
@api_view(['POST'])
@permission_classes([])
def register(request):
    user_name = request.data.get('name', '').strip()
    password = request.data.get('pass', '').strip()
    email = request.data.get('email', '').strip()
    code = request.data.get('code', '').strip()

    # 验证码校验
    cache_key = f"auth_code:register:{email}"
    cached_code = redis_client.get(cache_key)
    if not cached_code:
        return Response({
            "code": 400,
            "message": "验证码已过期或不存在"
        }, status=status.HTTP_400_BAD_REQUEST)

    if str(cached_code) != str(code):
        # redis_client.delete(cache_key)
        return Response({
            "code": 400,
            "message": "验证码错误"
        }, status=status.HTTP_400_BAD_REQUEST)

    # redis_client.delete(cache_key)
    # 检查重复（在事务外）
    if User.objects.filter(userName=user_name).exists():
        return Response({"code": 400, "message": "该用户名已被注册"}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(email=email).exists():
        return Response({"code": 400, "message": "该邮箱已被注册"}, status=status.HTTP_400_BAD_REQUEST)

    # 创建用户
    User.objects.create(
        userName=user_name,
        register=timezone.now(),
        email=email,
        password=make_password(password)
    )
    return Response({"code": 200, "currentTimeMillis": int(time.time() * 1000)}, status=status.HTTP_200_OK)


"""
@last-edit-date 2026-04-23
@author tyd
@desc 获取所有用户信息（分页）

"""
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_list(request):
    try:
        pageSize = int(request.GET.get('pageSize', 10))
        currentPage = int(request.GET.get('currentPage', 1))
    except (TypeError, ValueError):
        return Response({"code": 400, "message": "参数错误"}, status=status.HTTP_400_BAD_REQUEST)

    if pageSize <= 0 or currentPage <= 0:
        return Response({"code": 400, "message": "参数错误"}, status=status.HTTP_400_BAD_REQUEST)

    user_type = request.GET.get('userType', '').strip()
    user_status = request.GET.get('userStatus', '').strip()
    keyword = request.GET.get('keyword', '').strip()

    query = Q()
    if user_type:
        query &= Q(userType=user_type)
    if user_status:
        query &= Q(status=user_status)
    if keyword:
        query &= Q(
            Q(userName__icontains=keyword) |
            Q(email__icontains=keyword) |
            Q(phone__icontains=keyword)
        )

    queryset = User.objects.filter(query).order_by('register')
    count = queryset.count()
    users = queryset[(currentPage - 1) * pageSize: currentPage * pageSize]
    serializer = UserSerializer(users, many=True)
    for index, item in enumerate(serializer.data):
        item['s_id'] = index + 1 + (currentPage - 1) * pageSize

    return Response(data={
        "code": 200,
        "count": count,
        "users": serializer.data
    }, status=status.HTTP_200_OK)



@api_view(['PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_detail(request, id):
    if request.method == 'PUT':
        # 修改用户头像
        if request.data.get('avatar') is not None:
            user = User.objects.get(userId=int(id))
            today = timezone.localtime().strftime('%Y-%m-%d')
            avatar_change_key = f"user:{id}:avatar_change:{today}"
            last_change = redis_client.get(avatar_change_key)
            if last_change:
                return Response(data={
                    "code": 429,
                    "message": "每天只能修改一次头像，请明天再试"
                }, status=status.HTTP_429_TOO_MANY_REQUESTS)
            avatar = request.data.get('avatar')
            user.avatar = avatar
            user.save()
            redis_client.set(avatar_change_key, "1", ex=86400)
            serializer = UserSerializer(user)
            return Response(data={
                "user": serializer.data
            }, status=status.HTTP_200_OK)

        # 绑定邮箱
        elif request.data.get('email') is not None:
            email = request.data.get('email')
            password = request.data.get('password')
            user = User.objects.get(userId=int(id))
            # 判断密码是否正确
            user = authenticate(request, username=user.userName, password=password)
            if user:
                # 密码正确
                user.email = email  # 修改邮箱
                user.save()
                serializer = UserSerializer(user)
                return Response(data={"user": serializer.data}, status=status.HTTP_200_OK)
            else:
                # 密码错误, 返回错误码
                return Response(data={"errorMessage": "密码错误!"}, status=status.HTTP_400_BAD_REQUEST)

        # 修改用户名/性别/简介
        elif request.data.get('username') is not None:
            username = request.data.get('username')
            gender = request.data.get('gender')
            print(gender)
            introduce = request.data.get('introduce')
            user = User.objects.get(userId=id)
            # 修改了名字
            if user.userName != username:
                q_set = User.objects.filter(userName=username)
                if q_set:
                    return Response(data={"errorMessage": "该用户名已存在."}, status=status.HTTP_400_BAD_REQUEST)

            user.userSex, user.introduce, user.userName = gender, introduce, username
            user.save()
            return Response(data={
                "success": True,
                "user": UserSerializer(user).data
            }, status=status.HTTP_200_OK)

            
    elif request.method == "DELETE":
        try:
            print(id)
            obj = User.objects.get(userId=id)
            obj.delete()
            return Response(data={
                "success": True,
                "message": "用户删除成功",
                "deleted_id": id,
            },
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                data={
                    "success": False,
                    "error": "用户不存在",
                    "details": f"未找到ID为{id}的用户"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                data={
                    "success": False,
                    "error": "删除操作失败",
                    "details": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



"""
@last-edit-date 2026-04-30
@author tyd
@desc 修改用户状态

"""
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_user_statuts(request):
    userId = request.data.get('userId')
    userStatus = request.data.get('status')
    User.objects.filter(userId=userId).update(status=userStatus)
    return Response({'code': 200 }, 200)
