from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SchoolViewSet, ClassRoomViewSet

router = DefaultRouter()
router.register(r'schools', SchoolViewSet, basename='schools')
router.register(r'classrooms', ClassRoomViewSet, basename='classrooms')

urlpatterns = [
    path('', include(router.urls)),
]
