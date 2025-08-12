from rest_framework import serializers
from .models import Feedback
from accounts.serializers import UserSerializer
from students.serializers import StudentSerializer
from subjects.serializers import SubjectSerializer
from schools.models import TeachingAssignment
from accounts.models import CustomUser
from students.models import Student
from subjects.models import Subject

class FeedbackSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)
    parent = UserSerializer(read_only=True)
    student = StudentSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)

    parent_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(role='PARENT'),
        write_only=True,
        source='parent',
        required=True
    )
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(),
        write_only=True,
        source='student',
        required=True
    )
    subject_id = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(),
        write_only=True,
        source='subject',
        required=True
    )

    class Meta:
        model = Feedback
        fields = [
            'id',
            'teacher',
            'parent',
            'parent_id',
            'student',
            'student_id',
            'subject',
            'subject_id',
            'message',
            'created_at'
        ]
        read_only_fields = ['id', 'teacher', 'created_at']

    def validate(self, attrs):
        teacher = self.context['request'].user
        parent = attrs.get('parent')
        student = attrs.get('student')
        subject = attrs.get('subject')

        # Yoxla müəllim bu fənni hansısa sinifdə tədris edir
        if not TeachingAssignment.objects.filter(
            teacher=teacher,
            subject=subject
        ).exists():
            raise serializers.ValidationError({
                'non_field_errors': ["Siz bu fənni tədris etmirsiniz."]
            })

        # Valideyn-şagird əlaqəsini yoxla
        if student.parent != parent:
            raise serializers.ValidationError({
                'non_field_errors': ["Bu valideyn seçilmiş şagirdin valideyni deyil."]
            })

        return attrs

    def create(self, validated_data):
        validated_data['teacher'] = self.context['request'].user
        return super().create(validated_data)
