from rest_framework import serializers
from .models import School, ClassRoom

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'name', 'address', 'phone_number', 'email', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class ClassRoomSerializer(serializers.ModelSerializer):
    school = serializers.PrimaryKeyRelatedField(read_only=True)
    teachers = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )

    class Meta:
        model = ClassRoom
        fields = ['id', 'name', 'school', 'teachers', 'created_at']
        read_only_fields = ['id', 'created_at']
