from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import UserNotification
from .serializers import UserNotificationSerializer

class UserNotificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserNotification.objects.all()
    serializer_class = UserNotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = UserNotification.objects.filter(user=user).order_by('-created_at')
        return qs

    def get_object(self):
        # İcazəni düzgün yoxlamaq üçün override etdik
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj

    def retrieve(self, request, *args, **kwargs):
        # GET /user-notifications/{id}/ - oxundu kimi işarələnir və geri qaytarılır
        instance = self.get_object()
        if not instance.is_read:
            instance.is_read = True
            instance.save(update_fields=['is_read'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        # POST /user-notifications/{id}/mark-as-read/ - tək bildirişi oxunmuş et
        instance = self.get_object()
        if not instance.is_read:
            instance.is_read = True
            instance.save(update_fields=['is_read'])
        return Response({'detail': 'Marked as read'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        # POST /user-notifications/mark-all-as-read/ - bütün bildirişləri oxunmuş et
        qs = self.get_queryset().filter(is_read=False)
        updated_count = qs.update(is_read=True)
        return Response({'detail': f'{updated_count} notifications marked as read.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        # GET /user-notifications/unread-count/ - oxunmamış bildiriş sayı
        count = self.get_queryset().filter(is_read=False).count()
        return Response({'unread_count': count}, status=status.HTTP_200_OK)
