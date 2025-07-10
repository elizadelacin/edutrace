from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Student
from .serializers import StudentSerializer
from .permissions import IsAdminOrTeacherOfSchool, IsParentOfStudent

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related('school', 'classroom', 'parent').all()
    serializer_class = StudentSerializer

    def get_permissions(self):
        if self.action in ['list', 'create']:
            # List və Create: ADMIN və TEACHER
            return [IsAuthenticated(), IsAdminOrTeacherOfSchool()]
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            if self.request.user.role == 'PARENT':
                return [IsAuthenticated(), IsParentOfStudent()]
            return [IsAuthenticated(), IsAdminOrTeacherOfSchool()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return Student.objects.filter(school=user.school)
        if user.role == 'TEACHER':
            return Student.objects.filter(classroom__in=user.teaching_classrooms.all())
        if user.role == 'PARENT':
            return Student.objects.filter(parent=user)
        return Student.objects.none()

    def perform_create(self, serializer):
        # Yaradılan şagird avtomatik user.school ilə əlaqələnir
        serializer.save(school=self.request.user.school)
