from rest_framework.routers import DefaultRouter
from .views import AnnouncementViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'announcements', AnnouncementViewSet, basename='announcements')

urlpatterns = [
    path('', include(router.urls)),
]
