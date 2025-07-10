from rest_framework.permissions import BasePermission

class IsTeacherAndSubject(BasePermission):
    """
    Müəllim yalnız öz tədris etdiyi fənnlər üzrə assessment yarada/baxış edə bilər.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'TEACHER'

    def has_object_permission(self, request, view, obj):
        # Assessment obyektində subject və teacher əlaqəsi yoxlanır
        return obj.teacher == request.user

class IsResultTeacherOrStudent(BasePermission):
    """
    AssessmentResult-ə müəllim yalnız öz qiymətlərinə, şagird (gələcəkdə) yalnız öz nəticəsinə baxa bilər.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'TEACHER':
            return obj.assessment.teacher == request.user
        # PARENT/ADMIN/ şagird user öz nəticəsinə baxarsa
        return obj.student.user_id == request.user.id
