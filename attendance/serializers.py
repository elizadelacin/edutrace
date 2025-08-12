from rest_framework import serializers
from .models import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'student', 'student_name', 'subject', 'classroom', 'teacher', 'date', 'status']
        read_only_fields = ['id', 'teacher', 'date', 'student_name']

    def validate(self, attrs):
        user = self.context['request'].user

        student = attrs.get('student')
        subject = attrs.get('subject')
        classroom = attrs.get('classroom')

        if self.instance:
            if student is None:
                student = getattr(self.instance, 'student', None)
            if subject is None:
                subject = getattr(self.instance, 'subject', None)
            if classroom is None:
                classroom = getattr(self.instance, 'classroom', None)

        if user.role == 'TEACHER':
            if classroom is None or classroom not in user.teaching_classrooms.all():
                raise serializers.ValidationError(
                    "Bu sinif sizin dərs dediyiniz siniflərdən biri deyil."
                )

            if student is None or student.classroom != classroom:
                raise serializers.ValidationError(
                    "Bu şagird bu sinifə aid deyil."
                )

            if subject is None or subject not in user.teaching_subjects.all():
                raise serializers.ValidationError(
                    "Siz bu fənni tədris etmirsiniz."
                )

        return attrs
