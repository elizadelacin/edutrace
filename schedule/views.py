from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Schedule
from .serializers import ScheduleSerializer
from .permissions import IsAdminOrRelatedTeacherOrParent

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated, IsAdminOrRelatedTeacherOrParent]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return Schedule.objects.all()
        elif user.role == 'TEACHER':
            return Schedule.objects.filter(teacher=user)
        elif user.role == 'PARENT':
            classrooms = user.children.values_list('classroom', flat=True)
            return Schedule.objects.filter(classroom__in=classrooms)
        return Schedule.objects.none()
