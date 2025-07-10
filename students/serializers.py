from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    classroom_name = serializers.CharField(source='classroom.name', read_only=True)
    parent_username = serializers.CharField(source='parent.username', read_only=True)

    class Meta:
        model = Student
        fields = [
            'id', 'first_name', 'last_name',
            'school', 'classroom', 'classroom_name',
            'parent', 'parent_username', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'school', 'classroom_name', 'parent_username']
