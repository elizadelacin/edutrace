from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Only admins can create or edit. Others can only read.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'ADMIN'
