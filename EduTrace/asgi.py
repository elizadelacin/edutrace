import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import notifications.routing
from accounts.middleware import JWTAuthMiddleware  # Düzgün pathə diqqət edin

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EduTrace.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTAuthMiddleware(
        URLRouter(
            notifications.routing.websocket_urlpatterns
        )
    ),
})
