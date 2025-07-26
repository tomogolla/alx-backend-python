import logging
from datetime import datetime
from django.http import HttpResponse

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