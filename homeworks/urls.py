from rest_framework.routers import DefaultRouter
from .views import HomeworkViewSet

router = DefaultRouter()
router.register(r'homeworks', HomeworkViewSet, basename='homeworks')

urlpatterns = router.urls
