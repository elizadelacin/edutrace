from rest_framework.permissions import BasePermission

class IsTeacherOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['TEACHER', 'ADMIN']

class IsRelatedParent(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'ADMIN':
            return True
        if request.user.role == 'TEACHER':
            return obj.teacher == request.user
        if request.user.role == 'PARENT':
            return obj.student.parent == request.user
        return False
