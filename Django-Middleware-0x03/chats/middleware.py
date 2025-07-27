import time
from django.http import JsonResponse

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests = {}  # Tracks IP to list of timestamps
        self.limit = 5      # Max messages
        self.window = 60    # Time window in seconds

    def __call__(self, request):
        if request.method == 'POST' and request.path.startswith('/api/messages'):
            ip = self.get_ip(request)
            now = time.time()
            self.requests.setdefault(ip, [])
            # Filter timestamps within the last 60 seconds
            self.requests[ip] = [t for t in self.requests[ip] if now - t < self.window]

            if len(self.requests[ip]) >= self.limit:
                return JsonResponse(
                    {"error": "Rate limit exceeded. Max 5 messages per minute."},
                    status=429
                )

            self.requests[ip].append(now)

        return self.get_response(request)

    def get_ip(self, request):
        xff = request.META.get('HTTP_X_FORWARDED_FOR')
        return xff.split(',')[0] if xff else request.META.get('REMOTE_ADDR')
