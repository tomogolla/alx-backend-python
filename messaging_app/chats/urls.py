# messaging_app/chats/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from .views import ConversationViewSet, MessageViewSet

router = DefaultRouter()
# router.register(r'conversations', ConversationViewSet, basename='conversation')
# router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(['GET'])
def api_root(request, format=None):
    """
    API root endpoint that lists all available endpoints.
    """
    return Response({
        'conversations': reverse('conversation-list', request=request, format=format),
        'messages': reverse('message-list', request=request, format=format),
        'conversation_detail': reverse('conversation-detail', 
                                     kwargs={'pk': 'CONVERSATION_ID'}, 
                                     request=request, format=format),
        'message_detail': reverse('message-detail', 
                                kwargs={'pk': 'MESSAGE_ID'}, 
                                request=request, format=format),
        'search_users': reverse('conversation-search-users', 
                              request=request, format=format),
        'recent_messages': reverse('message-recent', 
                                 request=request, format=format),
    })
