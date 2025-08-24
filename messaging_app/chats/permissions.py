from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Conversation

class IsParticipantOfConversation(BasePermission):
    """
    Allows access only to authenticated users who are participants of a conversation.
    Applies to actions: GET, POST, PUT, PATCH, DELETE.
    """

    def has_permission(self, request, view):
        # Must be authenticated for any action
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Handle permission based on the object type
        conversation = None

        # Check if the object is a message or a conversation
        if hasattr(obj, 'conversation'):
            conversation = obj.conversation  # Message case
        elif hasattr(obj, 'participants'):
            conversation = obj  # Conversation case

        if conversation:
            is_participant = request.user in conversation.participants.all()
            if request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
                return is_participant

        return False