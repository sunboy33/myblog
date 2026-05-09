import time

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.conf import settings

from .utils import upload_to_qiniu, delete_from_qiniu
from backend.redis_client import redis_client
import redis


WEB_SETTINGS_KEY = "website:settings"

WEB_DEFAULT_CONFIG = {
    "title": "测试主题",
    "poem": "测试的句子",
    "author": "无",
    "icpNumber": "无",
    "contactEmail": "无",
    "copyright": "版权",
    "backGroundPreview": ""
}

"""
@last-eidt-date 2026-04-24
@author tyd
@desc 获取、修改网站配置信息

"""
@api_view(['GET', 'PUT'])
@permission_classes([])
def web_setting(request):
    if request.method == "GET":
        try:
            settings_data = redis_client.hgetall(WEB_SETTINGS_KEY)
            settings_data = {k: v for k, v in settings_data.items() if v}
            if settings_data:
                settings_dict = settings_data
            else:
                redis_client.hset(WEB_SETTINGS_KEY, mapping=WEB_DEFAULT_CONFIG)
                settings_dict = WEB_DEFAULT_CONFIG
        except redis.exceptions.ConnectionError as e:
            import logging
            logging.getLogger('api').warning(f"Redis connection failed: {e}, using default config")
            settings_dict = WEB_DEFAULT_CONFIG
        except Exception as e:
            import logging
            logging.getLogger('api').warning(f"Failed to get web settings: {e}")
            settings_dict = WEB_DEFAULT_CONFIG

        return Response({
            "code": 200,
            "data": settings_dict,
            "currentTimeMillis": int(time.time() * 1000)
        })
    elif request.method == "PUT":
        redis_client.hset(WEB_SETTINGS_KEY, mapping=request.data)
        return Response({
            "code": 200,
            "message": "更新成功",
            "currentTimeMillis": int(time.time() * 1000)
        }, status=status.HTTP_200_OK)



@api_view(["POST"])
def upload(request):
    """上传文件到七牛云"""
    file_name = request.POST.get("fileName")
    file_type = request.POST.get("type")
    file_data = request.FILES.get("file")
    old_src_path = request.POST.get("old_src_path")

    if not all([file_name, file_type, file_data]):
        return Response({
            "code": 400,
            "message": "缺少必要参数：fileName, type, file"
        }, status=status.HTTP_400_BAD_REQUEST)

    if file_data.size > settings.QINIU_MAX_FILE_SIZE:
        return Response({
            "code": 400,
            "message": f"文件大小不能超过 {settings.QINIU_MAX_FILE_SIZE // (1024 * 1024)}MB"
        }, status=status.HTTP_400_BAD_REQUEST)

    file_path = f"static/{file_type}/{file_name}"
    success, result = upload_to_qiniu(file_path, file_data, old_src_path)

    if success:
        return Response({
            "code": 200,
            "data": {"url": result},
            "message": "上传成功",
            "currentTimeMillis": int(time.time() * 1000)
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            "code": 500,
            "message": result
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])  # 添加认证类
@permission_classes([IsAuthenticated])  # 需要认证
def delete_media(request):
    """从七牛云删除文件"""
    file_url = request.data.get("fileUrl")
    if not file_url:
        return Response({
            "code": 400,
            "message": "缺少必要参数：fileUrl"
        }, status=status.HTTP_400_BAD_REQUEST)

    success = delete_from_qiniu(file_url)
    if success:
        return Response({
            "code": 200,
            "message": "删除成功",
            "currentTimeMillis": int(time.time() * 1000)
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            "code": 500,
            "message": "删除失败"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


