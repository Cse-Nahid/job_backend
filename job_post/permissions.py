from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Allow GET, HEAD or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Deny permission if user is not authenticated
        if not request.user.is_authenticated:
            return False


        # Check if the requesting user is the owner of the job post
        if request.user == obj.employer.user:
            return True
        else:
            return False

