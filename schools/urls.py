from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SchoolViewSet, ClassRoomViewSet, TeachingAssignmentViewSet

router = DefaultRouter()
router.register(r'schools', SchoolViewSet, basename='schools')
router.register(r'classrooms', ClassRoomViewSet, basename='classrooms')
router.register(r'teaching_assignments', TeachingAssignmentViewSet, basename='teachingassignments')

urlpatterns = [
    path('', include(router.urls)),
]
