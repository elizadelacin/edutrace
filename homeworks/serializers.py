from rest_framework import serializers
from .models import Homework

class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = '__all__'
        read_only_fields = ['teacher']
