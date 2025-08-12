from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import School, ClassRoom, TeachingAssignment
from .serializers import SchoolSerializer, ClassRoomSerializer, TeachingAssignmentSerializer
from .permissions import IsAdminOrReadOnly, IsAdminOrRelatedTeacherOrParentReadOnly

class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

class ClassRoomViewSet(viewsets.ModelViewSet):
    serializer_class = ClassRoomSerializer
    permission_classes = [IsAuthenticated, IsAdminOrRelatedTeacherOrParentReadOnly]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'ADMIN':
            return ClassRoom.objects.all()
        elif user.role == 'TEACHER':
            # Müəllim yalnız təyin olunduğu sinifləri görür
            return ClassRoom.objects.filter(teaching_assignments__teacher=user).distinct()
        elif user.role == 'PARENT':
            # Valideyn yalnız uşağının sinifini görür
            if hasattr(user, 'student') and user.student.classroom:
                return ClassRoom.objects.filter(pk=user.student.classroom.pk)
            return ClassRoom.objects.none()
        return ClassRoom.objects.none()

class TeachingAssignmentViewSet(viewsets.ModelViewSet):
    serializer_class = TeachingAssignmentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return TeachingAssignment.objects.all()
        elif user.role == 'TEACHER':
            # Müəllim yalnız öz təyinatlarını görür (yalnız GET icazəsi var)
            return TeachingAssignment.objects.filter(teacher=user)
        elif user.role == 'PARENT':
            # Valideyn yalnız uşağının sinifindəki təyinatları görür (yalnız GET icazəsi var)
            if hasattr(user, 'student') and user.student.classroom:
                return TeachingAssignment.objects.filter(classroom=user.student.classroom)
            return TeachingAssignment.objects.none()
        return TeachingAssignment.objects.none()
