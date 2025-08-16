from django.urls import path, include
from .views import UserViewSet, ConversationViewSet, MessageViewSet
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'conversations',ConversationViewSet, basename='conversation')

#nested urls
conversation_router = routers.NestedDefaultRouter(router,r'conversations', lookup='conversation')
conversation_router.register(r'messages', MessageViewSet, basename='conversation-messages')


urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(conversation_router.urls)),
]
