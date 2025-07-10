from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Assessment, AssessmentResult
from .serializers import AssessmentSerializer, AssessmentResultSerializer
from .permissions import IsTeacherAndSubject, IsResultTeacherOrStudent

class AssessmentViewSet(viewsets.ModelViewSet):
    serializer_class = AssessmentSerializer
    permission_classes = [IsAuthenticated, IsTeacherAndSubject]

    def get_queryset(self):
        return Assessment.objects.filter(teacher=self.request.user)

    def perform_create(self, serializer):
        subject = serializer.validated_data['subject']
        # müəllimin tədris etdiyi fənnlər siyahısında olduğunu yoxla
        if subject not in self.request.user.subjects.all():
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Yalnız öz fənniniz üzrə qiymətləndirmə edə bilərsiniz.")
        serializer.save(teacher=self.request.user)

class AssessmentResultViewSet(viewsets.ModelViewSet):
    serializer_class = AssessmentResultSerializer
    permission_classes = [IsAuthenticated, IsResultTeacherOrStudent]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'TEACHER':
            return AssessmentResult.objects.filter(assessment__teacher=user)
        if user.role == 'PARENT':
            return AssessmentResult.objects.filter(student__parent=user)
        return AssessmentResult.objects.none()
