from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FeedbackViewSet

router = DefaultRouter()
router.register(r'feedbacks', FeedbackViewSet, basename='feedbacks')

urlpatterns = [
    path('', include(router.urls)),
]
