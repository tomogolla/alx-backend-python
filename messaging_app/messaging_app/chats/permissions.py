from rest_framework import permissions


class IsSelf(permissions.BasePermission):
    """
    Custom permission to allow users to edit their own profile,
    or allow admin users to edit any profile.
    """

    def has_object_permission(self, request, view, obj):
        # Allow read-only access for any authenticated user (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow full access if the user is the owner of the object (i.e., editing their own profile)
        return obj == request.user

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to view/access it.
    Also restricts list view to only show conversations the user is a part of.
    """

    def has_permission(self, request, view):
        # Allow authenticated users to view lists/create conversations.
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Check if the user is a participant of the conversation object.
        return request.user in obj.participants.all()

class IsMessageOwnerOrIsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow the message sender OR a conversation participant
    to view/access a message.
    """

    def has_permission(self, request, view):
        # Allow authenticated users to view message lists/create messages.
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Define explicit write methods
        write_methods = ["PUT", "PATCH", "DELETE"]

        # Check if the user is a participant of the message's conversation first
        if request.user not in obj.conversation.participants.all():
            return False

        # If it's a read operation (GET, HEAD, OPTIONS), and the user is a participant, allow.
        if request.method in permissions.SAFE_METHODS:
            return True

        # For write operations (PUT, PATCH, DELETE),
        # only allow if the request method is one of the explicit write methods
        # AND the user is the original sender of the message.
        if request.method in write_methods:
            return obj.sender == request.user

        return False