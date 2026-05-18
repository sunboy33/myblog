import time
import logging
from django.utils import timezone

logger = logging.getLogger('api')


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        # 优先从 nginx 反向代理头获取真实 IP
        remote_addr = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('HTTP_X_REAL_IP') or request.META.get('REMOTE_ADDR')
        # 只取第一个 IP（多次代理时格式：client, proxy1, proxy2）
        if remote_addr and ',' in remote_addr:
            remote_addr = remote_addr.split(',')[0].strip()
        method = request.method
        path = request.path
        timestamp = timezone.localtime().strftime('%Y-%m-%d %H:%M:%S')

        response = self.get_response(request)
        duration = (time.time() - start_time) * 1000

        logger.info(
            f"{timestamp} | {remote_addr} | {method} {path} | {response.status_code} | {duration:.2f}ms"
        )
        return response
