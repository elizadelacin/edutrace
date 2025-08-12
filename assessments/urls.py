from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DailyAssessmentViewSet, ExamAssessmentViewSet

router = DefaultRouter()
router.register('daily', DailyAssessmentViewSet, basename='daily-assessments')
router.register('exam', ExamAssessmentViewSet, basename='exam-assessments')

urlpatterns = [
    path('assessments/', include(router.urls)),
]
