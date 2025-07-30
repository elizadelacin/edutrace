from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from .models import DailyAssessment, ExamAssessment
from .serializers import DailyAssessmentSerializer, ExamAssessmentSerializer
from .permissions import IsAdminOrRelatedTeacherOrParent

from students.models import Student
from subjects.models import Subject
from schools.models import ClassRoom

class DailyAssessmentViewSet(viewsets.ModelViewSet):
    queryset = DailyAssessment.objects.all()
    serializer_class = DailyAssessmentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrRelatedTeacherOrParent]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return DailyAssessment.objects.all()
        elif user.role == 'TEACHER':
            return DailyAssessment.objects.filter(teacher=user)
        elif user.role == 'PARENT':
            return DailyAssessment.objects.filter(student__parent=user)
        return DailyAssessment.objects.none()

    def perform_create(self, serializer):
        teacher = self.request.user
        classroom = serializer.validated_data['classroom']
        subject = serializer.validated_data['subject']
        student = serializer.validated_data['student']

        if teacher.role == 'TEACHER':
            if teacher not in classroom.teachers.all():
                raise PermissionDenied("Bu sinifdə dərs deməyə icazəniz yoxdur.")
            if subject.teacher != teacher:
                raise PermissionDenied("Bu fənni siz tədris etmirsiniz.")
            if student.classroom != classroom:
                raise PermissionDenied("Şagird bu sinifə aid deyil.")

        serializer.save(teacher=teacher)


class ExamAssessmentViewSet(viewsets.ModelViewSet):
    queryset = ExamAssessment.objects.all()
    serializer_class = ExamAssessmentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrRelatedTeacherOrParent]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return ExamAssessment.objects.all()
        elif user.role == 'TEACHER':
            return ExamAssessment.objects.filter(teacher=user)
        elif user.role == 'PARENT':
            return ExamAssessment.objects.filter(student__parent=user)
        return ExamAssessment.objects.none()

    def perform_create(self, serializer):
        teacher = self.request.user
        classroom = serializer.validated_data['classroom']
        subject = serializer.validated_data['subject']
        student = serializer.validated_data['student']

        if teacher.role == 'TEACHER':
            if teacher not in classroom.teachers.all():
                raise PermissionDenied("Bu sinifdə dərs deməyə icazəniz yoxdur.")
            if subject.teacher != teacher:
                raise PermissionDenied("Bu fənni siz tədris etmirsiniz.")
            if student.classroom != classroom:
                raise PermissionDenied("Şagird bu sinifə aid deyil.")

        serializer.save(teacher=teacher)

    @action(detail=False, methods=['post'], url_path='generate-yi')
    def generate_yi(self, request):
        user = request.user
        if user.role not in ['ADMIN', 'TEACHER']:
            return Response({"detail": "Only teachers or admin can perform this action."}, status=403)

        student_id = request.data.get('student')
        subject_id = request.data.get('subject')
        classroom_id = request.data.get('classroom')

        if not all([student_id, subject_id, classroom_id]):
            return Response({"detail": "student, subject, and classroom are required."}, status=400)

        try:
            student = Student.objects.get(id=student_id)
            subject = Subject.objects.get(id=subject_id)
            classroom = ClassRoom.objects.get(id=classroom_id)
        except (Student.DoesNotExist, Subject.DoesNotExist, ClassRoom.DoesNotExist):
            return Response({"detail": "Invalid student, subject or classroom."}, status=404)

        # Məntiq yoxlamaları (icazə yoxlamaları)
        if user.role == 'TEACHER':
            if user not in classroom.teachers.all():
                return Response({"detail": "Bu sinifə icazəniz yoxdur."}, status=403)
            if subject.teacher != user:
                return Response({"detail": "Bu fənni siz tədris etmirsiniz."}, status=403)
            if student.classroom != classroom:
                return Response({"detail": "Şagird bu sinifə aid deyil."}, status=403)

        from .utils import calculate_yearly_grade
        score = calculate_yearly_grade(student, subject, classroom)
        if score is None:
            return Response({"detail": "MS və ya BS qiymətləri yoxdur."}, status=400)

        ExamAssessment.objects.create(
            student=student,
            subject=subject,
            classroom=classroom,
            teacher=user,
            score=score,
            exam_type='YI'
        )
        return Response({"detail": f"YI qiyməti {score} uğurla yaradıldı."}, status=status.HTTP_201_CREATED)
