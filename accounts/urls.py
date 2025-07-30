from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, InvitationViewSet

router = DefaultRouter()
router.register(r'accounts', AccountViewSet, basename='accounts')
router.register(r'invitations', InvitationViewSet, basename='invitations')

urlpatterns = [
    path('', include(router.urls))
]