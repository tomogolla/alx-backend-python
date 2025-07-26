from rest_framework import permissions

class IsOwner(permissions.BasePermissions):
    """ 
    Custom permisions to only allow paticipants of a conversations to send, view, update, and delete message within the conversation.
    """
    def has_permision(self, request, view):
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