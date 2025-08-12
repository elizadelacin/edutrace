from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="EduTrace API",
        default_version='v1',
        description="Bu API müəllimlər, valideynlər və məktəb idarəçiləri üçün nəzərdə tutulmuşdur.",),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include('accounts.urls')),
    path('api/', include('schools.urls')),
    path('api/', include('students.urls')),
    path('api/', include('subjects.urls')),
    path('api/', include('assessments.urls')),
    path('api/', include('homeworks.urls')),
    path('api/', include('feedbacks.urls')),
    path('api/', include('attendance.urls')),
    path('api/', include('schedule.urls')),
    path('api/', include('announcements.urls')),
    path('api/', include('notifications.urls')),

    # Swagger & Redoc
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
