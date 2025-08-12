from rest_framework import serializers
from .models import Attendance
from schools.models import TeachingAssignment
from datetime import date

class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    date = serializers.DateField(required=False, default=date.today)  # İstifadəçi göndərməsə, bugünkü tarix

    class Meta:
        model = Attendance
        fields = ['id', 'student', 'student_name', 'subject', 'classroom', 'teacher', 'date', 'status']
        read_only_fields = ['id', 'teacher', 'student_name']

    def validate(self, attrs):
        user = self.context['request'].user

        # Əgər instance varsa, mövcud dəyərləri götür, yoxsa attrs-dən
        student = attrs.get('student') or getattr(self.instance, 'student', None)
        subject = attrs.get('subject') or getattr(self.instance, 'subject', None)
        classroom = attrs.get('classroom') or getattr(self.instance, 'classroom', None)

        if user.role == 'TEACHER':
            classroom_id = getattr(classroom, 'id', classroom)
            user_id = user.id

            if not TeachingAssignment.objects.filter(classroom_id=classroom_id, teacher_id=user_id).exists():
                raise serializers.ValidationError({
                    'non_field_errors': ['Bu sinif sizin dərs dediyiniz siniflərdən biri deyil.']
                })

            if student is None or student.classroom_id != classroom_id:
                raise serializers.ValidationError({
                    'non_field_errors': ['Bu şagird bu sinifə aid deyil.']
                })

            subject_id = getattr(subject, 'id', subject)
            if subject is None or not TeachingAssignment.objects.filter(
                    teacher_id=user_id,
                    classroom_id=classroom_id,
                    subject_id=subject_id
            ).exists():
                raise serializers.ValidationError({
                    'non_field_errors': ['Siz bu fənni tədris etmirsiniz.']
                })

        return attrs
