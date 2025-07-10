from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSchoolAdminOrReadOnly(BasePermission):
    """
    SAFE_METHODS (GET, HEAD, OPTIONS) üçün hər kəs <auth> ola bilər.
    Yazma əməliyyatları yalnız ADMIN rolundakı istifadəçilərə açıqdır.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.role == 'ADMIN'

class IsTeacherOfClassroom(BasePermission):
    """
    Detail səviyyəsində sinifə yalnız həmin sinifin müəllimləri baxa/yeniləyə bilər.
    """
    def has_object_permission(self, request, view, obj):
        return request.user.role == 'TEACHER' and obj.teachers.filter(id=request.user.id).exists()
