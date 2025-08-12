from rest_framework import viewsets
from .models import Announcement
from .serializers import AnnouncementSerializer
from .permissions import IsAdminOrReadOnly

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all().select_related('created_by').order_by('-created_at')
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return Announcement.objects.none()

        qs = super().get_queryset()
        if user.role == 'ADMIN':
            return qs
        elif user.role == 'TEACHER':
            return qs.filter(target_group__in=['ALL', 'TEACHERS'])
        elif user.role == 'PARENT':
            return qs.filter(target_group__in=['ALL', 'PARENTS'])
        return Announcement.objects.none()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        # Created_by dəyişməməlidir
        serializer.save()
