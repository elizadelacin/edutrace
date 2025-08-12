from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Attendance
from .serializers import AttendanceSerializer
from .permissions import IsAuthenticatedAndRelated

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated, IsAuthenticatedAndRelated]

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
        # Müəllim öz adına attendance yaradır
        serializer.save(teacher=self.request.user)

    def destroy(self, request, *args, **kwargs):
        # Müəllimlər silmək əməliyyatı edə bilməz
        if request.user.role == 'TEACHER':
            return Response(
                {'detail': 'Müəllimlər attendance-i silə bilməz.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)
