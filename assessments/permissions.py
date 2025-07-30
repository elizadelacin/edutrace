from rest_framework.permissions import BasePermission

class IsAdminOrRelatedTeacherOrParent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['ADMIN', 'TEACHER', 'PARENT']

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'ADMIN':
            return True
        elif request.user.role == 'TEACHER':
            return obj.teacher == request.user
        elif request.user.role == 'PARENT':
            return obj.student.parent == request.user
        return False
