from rest_framework import serializers
from .models import School, ClassRoom, TeachingAssignment
from accounts.serializers import UserSerializer
from subjects.serializers import SubjectSerializer

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'name', 'address', 'phone_number', 'email', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class ClassRoomSerializer(serializers.ModelSerializer):
    school = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ClassRoom
        fields = ['id', 'name', 'school', 'created_at']
        read_only_fields = ['id', 'created_at']

class TeachingAssignmentSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)
    classroom = ClassRoomSerializer(read_only=True)

    teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=UserSerializer.Meta.model.objects.filter(role='TEACHER'),
        write_only=True,
        source='teacher'
    )
    subject_id = serializers.PrimaryKeyRelatedField(
        queryset=SubjectSerializer.Meta.model.objects.all(),
        write_only=True,
        source='subject'
    )
    classroom_id = serializers.PrimaryKeyRelatedField(
        queryset=ClassRoom.objects.all(),
        write_only=True,
        source='classroom'
    )

    class Meta:
        model = TeachingAssignment
        fields = [
            'id',
            'teacher', 'teacher_id',
            'subject', 'subject_id',
            'classroom', 'classroom_id'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        return super().create(validated_data)
