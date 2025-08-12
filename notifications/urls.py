from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserNotificationViewSet

router = DefaultRouter()
router.register(r'user-notifications', UserNotificationViewSet, basename='user-notifications')

urlpatterns = [
    path('notifications/', include(router.urls)),
]
