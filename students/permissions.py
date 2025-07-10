from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrTeacherOfSchool(BasePermission):
    # - ADMIN rolundakı istifadəçi bütün şagirdləri görə/idarə edə bilər.
    # - TEACHER yalnız öz school-unun şagirdlərini görə bilər.

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['ADMIN', 'TEACHER']

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'ADMIN':
            return obj.school == request.user.school
        # TEACHER
        return obj.school == request.user.school and obj.classroom in request.user.teaching_classrooms.all()

class IsParentOfStudent(BasePermission):
    # Valideyn yalnız öz uşağının profiline baxa bilər.

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'PARENT'

    def has_object_permission(self, request, view, obj):
        return obj.parent_id == request.user.id
