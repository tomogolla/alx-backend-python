from rest_framework import permissions

class IsOwner(permissions.BasePermissions):
    """ 
    Custom permisions to only allow paticipants of a conversations to send, view, update, and delete message within the conversation.
    """
    def has_permission(self, request, view):
        #Allow only authenticated users to acess the API
        
        return request.user and request.user.is_athenticated
    
    
    def has_object_permission(self, request, view, obj):
        #check if the object is a conversation or a messagelinked to one
        user = request,user
        if hasattr(obj, 'participants'):
            # Its a conversation object
            return user in obj.participants.all()
        elif hasattr(obj, 'conversation'):
            # Its a message object
            return user in obj.conversation.participants.all()
        return False
    

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to authenticated users who are participants of the conversation.
    """

    def has_permission(self, request, view):
        # Ensure user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        if hasattr(obj, 'participants'):
            # Object is a Conversation
            return user in obj.participants.all()

        elif hasattr(obj, 'conversation'):
            # Object is a Message tied to a Conversation
            if request.method in ['GET', 'POST']:
                return user in obj.conversation.participants.all()
            elif request.method in ['PUT', 'PATCH', 'DELETE']:
                return user in obj.conversation.participants.all()

        return False