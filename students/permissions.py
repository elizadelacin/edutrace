from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'ADMIN'

    def has_object_permission(self, request, view, obj):
        return obj.school == request.user.school


class IsTeacherOfClassroom(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'TEACHER'

    def has_object_permission(self, request, view, obj):
        return (
            obj.school == request.user.school and
            obj.classroom in request.user.teaching_classrooms.all()
        )


class IsParentOfStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'PARENT'

    def has_object_permission(self, request, view, obj):
        return obj.parent_id == request.user.id
