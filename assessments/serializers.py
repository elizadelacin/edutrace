from rest_framework import serializers
from .models import DailyAssessment, ExamAssessment

class DailyAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyAssessment
        fields = '__all__'

class ExamAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamAssessment
        fields = '__all__'

    def validate(self, data):
        exam_type = data['exam_type']
        semester = data['semester']
        student = data['student']
        subject = data['subject']

        if exam_type == 'BS':
            # Ensure only one BS per semester
            exists = ExamAssessment.objects.filter(
                student=student,
                subject=subject,
                semester=semester,
                exam_type='BS'
            )
            if self.instance:
                exists = exists.exclude(id=self.instance.id)
            if exists.exists():
                raise serializers.ValidationError("Bu yarımildə artıq Böyük Summativ mövcuddur.")
        return data
