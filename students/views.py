from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from .models import Student
from .serializers import StudentSerializer
from .permissions import IsAdmin, IsTeacherOfClassroom, IsParentOfStudent

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related('school', 'classroom', 'parent').all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return Student.objects.filter(school=user.school)
        if user.role == 'TEACHER':
            return Student.objects.filter(classroom__in=user.teaching_classrooms.all())
        if user.role == 'PARENT':
            return Student.objects.filter(parent=user)
        return Student.objects.none()

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsAdmin()]
        if self.action in ['list']:
            if self.request.user.role == 'ADMIN':
                return [IsAuthenticated(), IsAdmin()]
            elif self.request.user.role == 'TEACHER':
                return [IsAuthenticated(), IsTeacherOfClassroom()]
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            if self.request.user.role == 'PARENT':
                return [IsAuthenticated(), IsParentOfStudent()]
            elif self.request.user.role == 'TEACHER':
                return [IsAuthenticated(), IsTeacherOfClassroom()]
            elif self.request.user.role == 'ADMIN':
                return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        user_school = self.request.user.school
        classroom = serializer.validated_data['classroom']

        # Classroom-un school-un user-in school ilə eyni olub-olmamasını yoxlayırıq
        if classroom.school != user_school:
            raise ValidationError("This classroom does not belong to your school.")

        # Student-i yaratarkən school-u avtomatik təyin edirik
        serializer.save(school=user_school)

