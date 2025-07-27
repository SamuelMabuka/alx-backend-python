# middleware.py
from datetime import datetime
from django.http import HttpResponseForbidden


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request path is for the messaging app (e.g., /chats/)
        if request.path.startswith('/chats/'):
            now = datetime.now().time()
            # Allowed time window: 18:00 (6PM) to 21:00 (9PM)
            if not (now >= datetime.strptime("18:00", "%H:%M").time() and
                    now <= datetime.strptime("21:00", "%H:%M").time()):
                return HttpResponseForbidden("Access to chats is restricted outside 6PM–9PM.")

        return self.get_response(request)
