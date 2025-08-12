from rest_framework import serializers
from .models import Feedback
from accounts.serializers import UserSerializer
from students.serializers import StudentSerializer
from subjects.serializers import SubjectSerializer
from accounts.models import CustomUser
from students.models import Student
from subjects.models import Subject

class FeedbackSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)
    parent = UserSerializer(read_only=True)
    student = StudentSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)

    parent_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.filter(role='PARENT'), write_only=True, source='parent', required=True)
    student_id = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), write_only=True, source='student', required=True)
    subject_id = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all(), write_only=True, source='subject', required=True)

    class Meta:
        model = Feedback
        fields = ['id', 'teacher', 'parent', 'parent_id', 'student', 'student_id', 'subject', 'subject_id', 'message', 'created_at']
        read_only_fields = ['id', 'teacher', 'created_at']

    def validate(self, attrs):
        teacher = self.context['request'].user
        parent = attrs.get('parent')
        student = attrs.get('student')
        subject = attrs.get('subject')

        if not teacher.teaching_subjects.filter(pk=subject.pk).exists():
            raise serializers.ValidationError("Siz bu fənni tədris etmirsiniz.")

        if student.parent != parent:
            raise serializers.ValidationError("Bu valideyn seçilmiş şagirdin valideyni deyil.")

        return attrs

    def create(self, validated_data):
        validated_data['teacher'] = self.context['request'].user
        return super().create(validated_data)
