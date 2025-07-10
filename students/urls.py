from rest_framework.routers import DefaultRouter
from django.urls import path, include

from EduTrace.urls import urlpatterns
from .views import StudentViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='students')

urlpatterns = [
    path('', include(router.urls))
]