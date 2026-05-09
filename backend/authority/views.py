import random
import time

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from backend.redis_client import redis_client
from .utils import send_email


def get_client_ip(request):
    """获取客户端真实IP"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
    return ip


def check_rate_limit(email, ip):
    """
    频率限制检查（统一使用 Redis）
    - 同一邮箱：60秒内只能发送1次
    - 同一IP：1小时内最多10次
    """
    # 邮箱频率限制
    email_key = f"rate_limit:email:{email}"
    if redis_client.exists(email_key):
        return False, "发送过于频繁，请稍后再试"

    # IP 频率限制
    ip_key = f"rate_limit:ip:{ip}"
    count = redis_client.get(ip_key)
    if count and int(count) >= 20:
        return False, "请求次数超限，请稍后再试"

    return True, ""


def record_send_time(email, ip):
    """记录发送时间（原子操作）"""
    # 邮箱：60秒内不能重复发送
    redis_client.setex(f"rate_limit:email:{email}", 60, "1")

    # IP：计数限制（原子递增）
    ip_key = f"rate_limit:ip:{ip}"
    pipe = redis_client.pipeline()
    pipe.incr(ip_key)
    pipe.expire(ip_key, 3600)
    pipe.execute()


@api_view(['POST'])
@permission_classes([])
def get_au_code(request):
    email = request.data.get('email', '').strip()
    type = request.data.get('type', '').strip()
    if type not in ['register', 'bindEmail', 'changePassword']:
        return Response({
            "code": 400,
            "message": "验证码类型不正确"
        }, status=status.HTTP_400_BAD_REQUEST)

    # 验证邮箱格式
    try:
        validate_email(email)
    except ValidationError:
        return Response({
            "code": 400,
            "message": "邮箱格式不正确"
        }, status=status.HTTP_400_BAD_REQUEST)

    # 获取客户端IP并检查频率限制
    client_ip = get_client_ip(request)
    allowed, msg = check_rate_limit(email, client_ip)
    if not allowed:
        return Response({
            "code": 429,
            "message": msg
        }, status=status.HTTP_429_TOO_MANY_REQUESTS)

    # 生成6位验证码
    code = f"{random.randint(0, 999999):06d}"

    # 存储验证码（5分钟有效期）
    cache_key = f"auth_code:{type}:{email}"
    redis_client.setex(cache_key, 300, code)

    # 记录发送时间
    record_send_time(email, client_ip)

    # 发送邮件
    try:
        if type == "register":
            subject = "【CODEJOURNEY】注册验证码"
        elif type == "bindEmail":
            subject = "【CODEJOURNEY】绑定邮箱验证码"
        else:
            subject = "【CODEJOURNEY】修改密码验证码"

        message = f"""
        您的验证码是：{code}
        有效时间：5分钟
        请勿将此验证码泄露给他人。
        """

        success = send_email(email, subject, message)
        if success:
            return Response({
                "code": 200,
                "message": "验证码已发送，请查看邮箱",
                "currentTimeMillis": int(time.time() * 1000)
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "code": 500,
                "message": "验证码发送失败，请稍后重试"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        return Response({
            "code": 500,
            "message": "系统错误，请稍后重试"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def verify(request):
    return Response({"code": 200})