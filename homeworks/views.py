from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Homework
from .serializers import HomeworkSerializer
from .permissions import IsAdminOrTeacherOrParentReadOnly
from students.models import Student

class HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Homework.objects.all().order_by('-created_at')
    serializer_class = HomeworkSerializer
    permission_classes = [IsAuthenticated, IsAdminOrTeacherOrParentReadOnly]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'ADMIN':
            return Homework.objects.all()

        elif user.role == 'TEACHER':
            return Homework.objects.filter(teacher=user)

        elif user.role == 'PARENT':
            children = Student.objects.filter(parent=user)
            classrooms = children.values_list('classroom', flat=True)
            return Homework.objects.filter(classroom__in=classrooms)

        return Homework.objects.none()

    def perform_create(self, serializer):
        teacher = self.request.user
        classroom = serializer.validated_data['classroom']
        subject = serializer.validated_data['subject']

        if teacher.role == 'TEACHER':
            if teacher not in classroom.teachers.all():
                raise PermissionDenied("Bu sinif üçün tapşırıq əlavə etmək icazəniz yoxdur.")
            if subject.teacher != teacher:
                raise PermissionDenied("Bu fənn üzrə tapşırıq əlavə etmək icazəniz yoxdur.")

        serializer.save(teacher=teacher)
