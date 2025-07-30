from rest_framework.permissions import BasePermission

class IsAdminOrRelatedTeacherOrParent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'ADMIN':
            return True
        if request.user.role == 'TEACHER':
            return obj.teacher == request.user
        if request.user.role == 'PARENT':
            return obj.classroom.students.filter(parent=request.user).exists()
        return False
