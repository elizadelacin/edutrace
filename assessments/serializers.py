from rest_framework import serializers
from .models import DailyAssessment, ExamAssessment

class DailyAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyAssessment
        fields = '__all__'
        read_only_fields = ['teacher', 'date']

class ExamAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamAssessment
        fields = '__all__'
        read_only_fields = ['teacher', 'date']
