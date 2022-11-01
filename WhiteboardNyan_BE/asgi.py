"""
ASGI config for WhiteboardNyan_BE project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
import django

from django.core.asgi import get_asgi_application
from channels.http import AsgiHandler
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import WhiteboardNyan_BE.WhiteboardNyan_App.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WhiteboardNyan_BE.settings")

django.setup()
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            WhiteboardNyan_BE.WhiteboardNyan_App.routing.websocket_urlpatterns
        )
    ),
})
#application = get_asgi_application()
