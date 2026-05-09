import time
import logging
from django.utils import timezone

logger = logging.getLogger('api')


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        remote_addr = request.META.get('REMOTE_ADDR')
        method = request.method
        path = request.path
        timestamp = timezone.localtime().strftime('%Y-%m-%d %H:%M:%S')

        response = self.get_response(request)
        duration = (time.time() - start_time) * 1000

        logger.info(
            f"{timestamp} | {remote_addr} | {method} {path} | {response.status_code} | {duration:.2f}ms"
        )
        return response
