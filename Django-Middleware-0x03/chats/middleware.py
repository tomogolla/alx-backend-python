import logging
from datetime import datetime, timedelta
from django.http import HttpResponse, JsonResponse
from collections import defaultdict
# set up logging to file

logger = logging.getLogger("request_logger")
handler = logging.FileHandler("requests.log")
formatter = logging.Formatter('%(message)s')

handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        response = self.get_response(request)
        return response
    

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, *request):
        current_hour = datetime.now().hour
        
        # allow access between 6PM and 9PM
        if not (18 <= current_hour < 21):
            return HttpResponseForbidden("Access to chats is restricted between 6 PM and 9 PM.")
        return self.get_response(request)
    
    
class OffesiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_times = defaultdict(list)
    
    def __call__(self, request):
        if request.method == 'POST' and '/chats/' in request.path:
            ip = self.get_client_ip(request)
            now = datetime.now()
            one_minute_ago = now - timedelta(minutes=1)
            
            
            self.request_times[ip] = [
                timestamp for timestamp in self.request_times[ip]
                if timestamp > one_minute_ago
            ]
            
            if len(self.request_times[ip] >= 5):
                return JsonResponse(
                    {'error': 'Rate limit exceeded. You can only send 5 messages per minute'},
                    status=429
                )
            self.request_times[ip].append(now)
        return self.get_response(request)
    
    
    def get_client_ip(self, request):
        x_forwaded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwaded_for:
            return x_forwaded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')