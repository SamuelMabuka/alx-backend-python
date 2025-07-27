# middleware.py
from datetime import datetime, timedelta
from django.http import HttpResponseTooManyRequests


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_message_log = {}  # {ip_address: [timestamps]}

    def __call__(self, request):
        # Only rate-limit POST requests to chat endpoints
        if request.path.startswith('/chats/') and request.method == 'POST':
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Get or initialize the list of timestamps for this IP
            timestamps = self.ip_message_log.get(ip, [])

            # Filter timestamps to keep only those within the last 60 seconds
            one_minute_ago = now - timedelta(minutes=1)
            timestamps = [ts for ts in timestamps if ts > one_minute_ago]

            if len(timestamps) >= 5:
                return HttpResponseTooManyRequests("Rate limit exceeded: Max 5 messages per minute.")

            # Append current timestamp and update the log