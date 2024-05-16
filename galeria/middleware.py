# middleware.py

import time
from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.http import HttpResponseServerError

class TimeoutMiddleware:
    def __init__(self, get_response=None):
        self.get_response = get_response
        if not settings.DEBUG:
            raise MiddlewareNotUsed("TimeoutMiddleware is only available in DEBUG mode.")
        try:
            self.http_timeout = settings.HTTP_TIMEOUT
        except AttributeError:
            raise MiddlewareNotUsed("HTTP_TIMEOUT setting is not defined.")

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        elapsed_time = time.time() - start_time
        if elapsed_time > self.http_timeout:
            return HttpResponseServerError("HTTP request timeout")
        return response
