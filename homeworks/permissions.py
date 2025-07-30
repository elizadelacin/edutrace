from rest_framework.permissions import BasePermission, SAFE_METHODS
from students.models import Student

class IsAdminOrTeacherOrParentReadOnly(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        if user.role in ['ADMIN', 'TEACHER']:
            return True

        if user.role == 'PARENT':
            return request.method in SAFE_METHODS  # Yalnız baxa bilər

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.role == 'ADMIN':
            return True

        if user.role == 'TEACHER':
            return obj.teacher == user

        if user.role == 'PARENT':
            return request.method in SAFE_METHODS and obj.classroom.students.filter(parent=user).exists()

        return False
