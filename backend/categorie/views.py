

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Count

from .models import ArticleLabel, ArticleType
from .serializers import ArticleTypeSerializer,ArticleLabelSerializer



@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@authentication_classes([])  # 添加认证类
@permission_classes([])  # 需要认证
def type_crud(request):
    if request.method == 'PUT':
        id = request.data['id']
        type = request.data['type']
        desc = request.data['desc']
        priority = request.data['priority']
        ArticleType.objects.filter(id=id).update(type=type, desc=desc, priority=priority)
        return Response({'success': True}, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        print(request.data)
        id = request.data.get('id')
        type = ArticleType.objects.get(id=id)
        type.delete()
        return Response({'success': True}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        type = request.data['type']
        desc = request.data['desc']
        priority = request.data['priority']
        q_set = ArticleType.objects.filter(type=type)
        if len(q_set) == 0:
            ArticleType.objects.create(type=type, desc=desc, priority=priority)
            return Response({'success': True}, status=status.HTTP_200_OK)
        return Response({"message": "该分类已存在!"}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        try:
            types = ArticleType.objects.annotate(article_count=Count('articles')).all()
            serializer = ArticleTypeSerializer(types, many=True)
            for index, item in enumerate(serializer.data):
                item['s_id'] = index + 1
            return Response(data={
                "types": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={
                "success": False,
                "message": "获取文章类型信息失败"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])  # 添加认证类
@permission_classes([IsAuthenticated])  # 需要认证
def delete_sort(request, id):
    type = ArticleType.objects.get(id=id)
    type.delete()
    return Response({'success': True}, status=status.HTTP_200_OK)
        



@api_view(['POST', 'GET', 'PUT', 'DELETE'])
def label_crud(request):
    if request.method == "GET":
        try:
            labels = ArticleLabel.objects.select_related('type').annotate(
                article_count=Count('labels'))
            serializer = ArticleLabelSerializer(labels, many=True)
            for index, item in enumerate(serializer.data):
                item['s_id'] = index + 1
            return Response(data={
                "success": True,
                "labels": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            return Response(data={
                "success": False,
                "message": "获取标签信息失败",
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    if request.method == "POST":
        try:
            data = request.data
            type_id = ArticleType.objects.get(type=data['type']).id
            for label in data['label']:
                q_set = ArticleLabel.objects.filter(label=label)
                if len(q_set) == 0:
                    ArticleLabel.objects.create(label=label, type_id=type_id)
                else:
                    continue
            return Response(data={"success": True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={
                "success": False,
                "message": "标签添加失败",
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
