from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser, Invitation
from .tasks import send_activation_email
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from .tokens import password_reset_token_generator

class UserSerializer(serializers.ModelSerializer):
    school = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'role', 'school', 'is_email_verified',)
        read_only_fields = ('is_email_verified', 'role')

class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = '__all__'

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
        user = CustomUser.objects.create_user(**validated_data, is_email_verified=False,)
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
        data.update({
            'role': user.role,
        })
        return data

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value

class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    uidb64 = serializers.CharField()
    token = serializers.CharField()

    def validate(self, attrs):
        try:
            uid = force_str(urlsafe_base64_decode(attrs['uidb64']))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            raise serializers.ValidationError('Invalid uid')

        if not password_reset_token_generator.check_token(user, attrs['token']):
            raise serializers.ValidationError('Invalid or expired token')

        attrs['user'] = user
        return attrs

    def save(self):
        user = self.validated_data['user']
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
