from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Yalnız admin istənilən əməliyyat edə bilər,
    digərləri yalnız oxuya bilər.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.role == 'ADMIN'

    def has_object_permission(self, request, view, obj):
        # Oxumaq üçün hamıya icazə, yazmaq üçün admin lazımdır
        if request.method in SAFE_METHODS:
            return True
        return request.user.role == 'ADMIN'
