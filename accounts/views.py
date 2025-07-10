from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, RegisterSerializer, CustomTokenSerializer
from .permissions import IsSelfOrAdmin

User = get_user_model()

class AccountViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['register', 'login', 'activate']:
            return [AllowAny()]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            return [IsAuthenticated(), IsSelfOrAdmin()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        return TokenObtainPairView.as_view(serializer_class=CustomTokenSerializer)(request._request)

    @action(detail=False, methods=['get'], url_path='activate/(?P<uid>[^/.]+)/(?P<token>[^/.]+)')
    def activate(self, request, uid, token):
        user = get_object_or_404(User, pk=uid)
        if settings.EMAIL_VERIFICATION_TOKEN_GENERATOR.check_token(user, token):
            user.is_email_verified = True
            user.save()
            return HttpResponse("Email verified.")
        return HttpResponse("Invalid or expired activation link.", status=400)
