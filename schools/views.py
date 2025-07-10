from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import School, ClassRoom
from .serializers import SchoolSerializer, ClassRoomSerializer
from .permissions import IsSchoolAdminOrReadOnly, IsTeacherOfClassroom

class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = [IsAuthenticated, IsSchoolAdminOrReadOnly]

class ClassRoomViewSet(viewsets.ModelViewSet):
    serializer_class = ClassRoomSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Yaradılması/yenilənməsi yalnız ADMIN-lər üçündür
            return [IsAuthenticated(), IsSchoolAdminOrReadOnly()]
        if self.action in ['retrieve']:
            # Retrieve səviyyəsində müəllimə baxış icazəsi
            return [IsAuthenticated(), IsTeacherOfClassroom()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            # Admin öz məktəbinin siniflərini görsün
            return ClassRoom.objects.filter(school=user.school)
        elif user.role == 'TEACHER':
            # Müəllim yalnız tədris etdiyi sinifləri görsün
            return user.teaching_classrooms.all()
        return ClassRoom.objects.none()

    def perform_create(self, serializer):
        # Sinif yaratma zamanı avtmat olaraq istifadəçinin school sahəsi təyin olunur
        serializer.save(school=self.request.user.school)
