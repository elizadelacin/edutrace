# serializers.py
from rest_framework import serializers
from .models import Feedback
from accounts.models import CustomUser
from students.models import Student
from subjects.models import Subject
from schools.models import TeachingAssignment
from accounts.serializers import UserSerializer
from students.serializers import StudentSerializer
from subjects.serializers import SubjectSerializer

class FeedbackSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)
    parent = UserSerializer(read_only=True)
    student = StudentSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)

    parent_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(role='PARENT'),
        write_only=True,
        source='parent'
    )
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(),
        write_only=True,
        source='student'
    )
    subject_id = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(),
        write_only=True,
        source='subject'
    )

    class Meta:
        model = Feedback
        fields = [
            'id', 'teacher', 'parent', 'parent_id',
            'student', 'student_id', 'subject', 'subject_id',
            'message', 'created_at'
        ]
        read_only_fields = ['id', 'teacher', 'created_at']

    def validate(self, attrs):
        teacher = self.context['request'].user
        parent = attrs['parent']
        student = attrs['student']
        subject = attrs['subject']

        # Şagirdin sinfi yoxlanır
        classroom = getattr(student, 'classroom', None)
        if not classroom:
            raise serializers.ValidationError({
                'non_field_errors': ["Bu şagirdin sinfi təyin olunmayıb."]
            })

        # Müəllim + fənn + sinif uyğunluğu yoxlanır
        if not TeachingAssignment.objects.filter(
            teacher=teacher,
            subject=subject,
            classroom=classroom
        ).exists():
            raise serializers.ValidationError({
                'non_field_errors': ["Siz bu fənni bu sinifdə tədris etmirsiniz."]
            })

        # Valideyn-şagird əlaqəsi
        if student.parent != parent:
            raise serializers.ValidationError({
                'non_field_errors': ["Bu valideyn seçilmiş şagirdin valideyni deyil."]
            })

        return attrs

    def create(self, validated_data):
        validated_data['teacher'] = self.context['request'].user
        return super().create(validated_data)
