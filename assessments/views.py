from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import DailyAssessment, ExamAssessment
from .serializers import DailyAssessmentSerializer, ExamAssessmentSerializer
from .permissions import IsAdminOrRelatedTeacherOrParent
from .utils import calculate_yekun_illik
from django.utils import timezone
from students.models import Student

class DailyAssessmentViewSet(viewsets.ModelViewSet):
    queryset = DailyAssessment.objects.all()
    serializer_class = DailyAssessmentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrRelatedTeacherOrParent]

    def get_queryset(self):
        user = self.request.user

        if user.role == "ADMIN":
            return DailyAssessment.objects.all()

        elif user.role == "TEACHER":
            return DailyAssessment.objects.filter(teacher=user)

        elif user.role == "PARENT":
            return DailyAssessment.objects.filter(student__parent=user)

        return DailyAssessment.objects.none()

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


class ExamAssessmentViewSet(viewsets.ModelViewSet):
    queryset = ExamAssessment.objects.all()
    serializer_class = ExamAssessmentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrRelatedTeacherOrParent]

    def get_queryset(self):
        user = self.request.user

        if user.role == "ADMIN":
            return ExamAssessment.objects.all()

        elif user.role == "TEACHER":
            return ExamAssessment.objects.filter(teacher=user)

        elif user.role == "PARENT":
            return ExamAssessment.objects.filter(student__parent=user)

        return ExamAssessment.objects.none()

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

    @action(detail=False, methods=['post'], url_path='generate-yi')
    def generate_yekun_illik(self, request):
        student_id = request.data.get("student_id")
        subject_id = request.data.get("subject_id")

        if not student_id or not subject_id:
            return Response(
                {"error": "student_id və subject_id mütləqdir."},
                status=status.HTTP_400_BAD_REQUEST
            )

        student = Student.objects.filter(id=student_id).first()
        if not student:
            return Response(
                {"error": "Belə bir şagird mövcud deyil."},
                status=status.HTTP_404_NOT_FOUND
            )

        classroom = student.classroom  # Bu dəyişəni istifadə edə bilərsən

        existing_yi = ExamAssessment.objects.filter(
            student_id=student_id,
            subject_id=subject_id,
            exam_type='YI'
        ).first()

        if existing_yi:
            return Response(
                {"error": "Bu şagird və fənn üçün artıq yekun illik qiymət mövcuddur."},
                status=status.HTTP_400_BAD_REQUEST
            )

        final_score = calculate_yekun_illik(student_id, subject_id)

        if final_score is None:
            return Response(
                {"error": "Hesablama üçün kifayət qədər məlumat yoxdur."},
                status=status.HTTP_400_BAD_REQUEST
            )

        assessment = ExamAssessment.objects.create(
            student_id=student_id,
            subject_id=subject_id,
            teacher=request.user,
            exam_type='YI',
            score=final_score,
            date=timezone.now().date(),
            classroom = student.classroom
        )

        serializer = self.get_serializer(assessment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
