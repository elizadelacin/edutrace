from rest_framework import serializers
from .models import Schedule

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['id', 'classroom', 'subject', 'teacher', 'weekday', 'time']
        read_only_fields = ['id']
