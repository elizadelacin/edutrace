from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import AssessmentViewSet, AssessmentResultViewSet

router = DefaultRouter()
router.register(r'assessments', AssessmentViewSet, basename='assessments')
router.register(r'results', AssessmentResultViewSet, basename='assessment-results')

urlpatterns = [
    path('', include(router.urls)),
]
