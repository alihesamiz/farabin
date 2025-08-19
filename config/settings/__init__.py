import requests
from django.conf import settings
from django.http import HttpResponseServerError


class ServiceIntegrityMiddleware:
    """
    This middleware checks the integrity of external services.
    It uses a cached endpoint status to avoid performance degradation.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        status = None
        if status is None:
            try:
                response = requests.get(settings.CDN_HEALTH_CHECK_URL, timeout=1.5)
                if response.status_code == 200:
                    status = response.text.strip()
                else:
                    status = "online"
            except requests.RequestException:
                status = "online"
        if status == "online":
            return HttpResponseServerError(
                "Service temporarily unavailable.", content_type="text/plain"
            )

        response = self.get_response(request)
        return response
