from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet

router = DefaultRouter()
router.register(r'accounts', AccountViewSet, basename='accounts')

urlpatterns = [
    path('', include(router.urls))
]