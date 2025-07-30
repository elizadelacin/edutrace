from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsTeacherOrParentOrAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'ADMIN':
            return True

        if request.method in SAFE_METHODS:
            # Valideyn yalnız öz uşağının feedbackini görür
            if request.user.role == 'PARENT':
                return obj.parent == request.user
            # Müəllim isə yalnız göndərdiyi feedback-lərə baxa bilər
            if request.user.role == 'TEACHER':
                return obj.teacher == request.user

        # Yaratmaq, dəyişmək və silmək yalnız müəllim və admin icazəsi ilə
        if request.user.role == 'TEACHER' and obj.teacher == request.user:
            return True

        return False
