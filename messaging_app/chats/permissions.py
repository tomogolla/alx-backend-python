from res_framework import permissions

class IsOwner(permissions.BasePermissions):
    """ 
    Custom permisions to only allow users to access their own messages or conversations.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or obj.sender == request.user or obj.reciever == request.user