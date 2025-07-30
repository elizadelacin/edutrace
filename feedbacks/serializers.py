from rest_framework import serializers
from .models import Feedback
from accounts.serializers import UserSerializer
from students.serializers import StudentSerializer
from accounts.models import CustomUser
from students.models import Student

class FeedbackSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)
    parent = UserSerializer(read_only=True)
    student = StudentSerializer(read_only=True)

    parent_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(role='PARENT'), write_only=True, source='parent', required=True
    )
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(), write_only=True, source='student', required=True
    )

    class Meta:
        model = Feedback
        fields = [
            'id', 'teacher', 'parent', 'parent_id', 'student', 'student_id',
            'message', 'created_at'
        ]
        read_only_fields = ['id', 'teacher', 'created_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from accounts.models import CustomUser
        from students.models import Student

        self.fields['parent_id'].queryset = CustomUser.objects.filter(role='PARENT')
        self.fields['student_id'].queryset = Student.objects.all()

    def validate(self, attrs):
        teacher = self.context['request'].user
        parent = attrs.get('parent')
        student = attrs.get('student')

        # Valideynin şagirdin valideyni olub-olmamasını yoxla
        if not student.parents.filter(pk=parent.pk).exists():
            raise serializers.ValidationError("Bu valideyn seçilmiş şagirdin valideyni deyil.")
        return attrs

    def create(self, validated_data):
        validated_data['teacher'] = self.context['request'].user
        return super().create(validated_data)
