from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Admin POST, PUT, DELETE edə bilər.
    Digərləri yalnız oxuya bilər.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'ADMIN'

class IsAdminOrRelatedTeacherOrParentReadOnly(BasePermission):
    """
    Admin: tam giriş.
    Müəllim və valideynlər: yalnız oxuya bilərlər.
    Objekti müəllim və valideyn uyğunluğu ilə yoxlayır.
    """
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        if user.role == 'ADMIN':
            return True
        elif user.role in ['TEACHER', 'PARENT']:
            # Müəllim və valideynlər yalnız oxuya bilərlər
            return request.method in SAFE_METHODS
        return False

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.role == 'ADMIN':
            return True
        elif user.role == 'TEACHER':
            # Müəllim yalnız öz təyinatı olan siniflərə baxa bilər
            return obj.teaching_assignments.filter(teacher=user).exists()
        elif user.role == 'PARENT':
            # Valideyn yalnız uşağının sinifinə baxa bilər
            return hasattr(user, 'student') and user.student.classroom == obj
        return False
