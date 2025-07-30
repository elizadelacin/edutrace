from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Attendance
from .serializers import AttendanceSerializer
from .permissions import IsTeacherOrAdmin, IsRelatedParent

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin, IsRelatedParent]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return Attendance.objects.all()
        elif user.role == 'TEACHER':
            return Attendance.objects.filter(teacher=user)
        elif user.role == 'PARENT':
            return Attendance.objects.filter(student__parent=user)
        return Attendance.objects.none()

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)
