from rest_framework import serializers
from .models import Assessment, AssessmentResult

class AssessmentResultSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.__str__', read_only=True)

    class Meta:
        model = AssessmentResult
        fields = ['id', 'student', 'student_name', 'score', 'feedback', 'created_at']
        read_only_fields = ['id', 'created_at', 'student_name']

class AssessmentSerializer(serializers.ModelSerializer):
    results = AssessmentResultSerializer(many=True, read_only=True)

    class Meta:
        model = Assessment
        fields = ['id', 'title', 'subject', 'teacher', 'classroom', 'date', 'created_at', 'results']
        read_only_fields = ['id', 'teacher', 'created_at']
