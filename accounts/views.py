from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Invitation
from .serializers import UserSerializer, RegisterSerializer, CustomTokenSerializer, InvitationSerializer
from .permissions import IsSelfOrAdmin
from .tasks import send_activation_email
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

User = get_user_model()

class InvitationViewSet(viewsets.ModelViewSet):
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        invitation = serializer.save()
        from .tasks import send_invitation_email
        send_invitation_email.delay(invitation.id)

    def update(self, request, *args, **kwargs):
        # Update (PUT/PATCH) qadağandır — admin yalnız yaradıb, sonra email göndərir
        return Response({"detail": "Invitation update is not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class AccountViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['register', 'login', 'activate']:
            return [AllowAny()]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            return [IsAuthenticated(), IsSelfOrAdmin()]
        elif self.action in ['teachers', 'parents']:
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_activation_email.delay(user.id)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        return TokenObtainPairView.as_view(serializer_class=CustomTokenSerializer)(request._request)

    @action(detail=False, methods=['get'], url_path='activate/(?P<uid>[^/.]+)/(?P<token>[^/.]+)')
    def activate(self, request, uid, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = get_object_or_404(User, pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return HttpResponse("Invalid activation link.", status=400)

        if settings.EMAIL_VERIFICATION_TOKEN_GENERATOR.check_token(user, token):
            user.is_email_verified = True
            user.save()
            return HttpResponse("Email verified.")
        else:
            return HttpResponse("Invalid or expired activation link.", status=400)

    @action(detail=False, methods=['get'])
    def teachers(self, request):
        teachers = User.objects.filter(role='TEACHER')
        serializer = self.get_serializer(teachers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def parents(self, request):
        parents = User.objects.filter(role='PARENT')
        serializer = self.get_serializer(parents, many=True)
        return Response(serializer.data)
