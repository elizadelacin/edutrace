from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthenticatedAndRelated(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        # Valideynlər yalnız oxuya bilər
        if user.role == 'PARENT':
            return request.method in SAFE_METHODS

        # Müəllim və Admin hərəkət edə bilər
        if user.role in ['TEACHER', 'ADMIN']:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.role == 'ADMIN':
            return True

        if user.role == 'TEACHER':
            return obj.teacher == user

        if user.role == 'PARENT':
            return obj.student.parent == user

        return False
