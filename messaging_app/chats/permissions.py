from rest_framework import permissions
from .models import Conversation

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    This permission applies to all methods, including GET, POST, PUT, PATCH, and DELETE.
    """
    def has_permission(self, request, view):
        # Allow access if user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # 'obj' here is either a Conversation or a Message instance.
        conversation = obj if isinstance(obj, Conversation) else obj.conversation
        
        # Check if the requesting user is in the conversation's participants.
        return request.user in conversation.participants.all()