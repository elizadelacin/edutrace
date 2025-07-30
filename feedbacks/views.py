from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Feedback
from .serializers import FeedbackSerializer
from .permissions import IsTeacherOrParentOrAdmin

class FeedbackViewSet(viewsets.ModelViewSet):
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated, IsTeacherOrParentOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return Feedback.objects.all()
        elif user.role == 'TEACHER':
            return Feedback.objects.filter(teacher=user)
        elif user.role == 'PARENT':
            return Feedback.objects.filter(parent=user)
        return Feedback.objects.none()

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)
