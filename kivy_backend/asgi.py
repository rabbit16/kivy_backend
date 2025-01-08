"""
ASGI config for kivy_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os


from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kivy_backend.settings")

from channels.routing import ProtocolTypeRouter, URLRouter
from . import routing

# application = get_asgi_application()
# websocket
application = ProtocolTypeRouter({
    # 处理http请求
    'http': get_asgi_application(),
    # 处理websocket请求
    'websocket': URLRouter(routing.websocket_urlpatterns)})
