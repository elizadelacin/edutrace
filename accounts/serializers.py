from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser, Invitation
from .tasks import send_activation_email
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    school = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'role', 'school', 'is_email_verified', 'is_approved')
        read_only_fields = ('is_email_verified', 'is_approved', 'role')

class RegisterSerializer(serializers.ModelSerializer):
    invite_code = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'invite_code')
        extra_kwargs = {
            'password': {'write_only': True, 'validators': [validate_password]}
        }

    def validate(self, attrs):
        try:
            self.invite = Invitation.objects.get(
                code=attrs['invite_code'],
                email=attrs['email'],
                used=False
            )
        except Invitation.DoesNotExist:
            raise serializers.ValidationError("Invalid or used invitation code.")
        return attrs

    def create(self, validated_data):
        validated_data['role'] = self.invite.role
        validated_data['school'] = self.invite.school
        validated_data.pop('invite_code')
        user = CustomUser.objects.create_user(**validated_data, is_email_verified=False, is_approved=False)
        self.invite.used = True
        self.invite.save()
        send_activation_email.delay(user.pk)
        return user

class CustomTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        if not user.is_email_verified:
            raise serializers.ValidationError("Email not verified.")
        if not user.is_approved:
            raise serializers.ValidationError("Account not approved by admin.")
        data.update({
            'role': user.role,
        })
        return data
