from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet, UserNotificationViewSet

router = DefaultRouter()
router.register('notifications', NotificationViewSet, basename='notification')
router.register('user-notifications', UserNotificationViewSet, basename='user-notification')

urlpatterns = router.urls
