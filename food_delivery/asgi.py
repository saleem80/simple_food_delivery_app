"""
ASGI config for food_delivery project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_delivery.settings')

# Lazy application loader to avoid premature imports
class ASGIApplication:
    def __init__(self):
        self._application = None

    async def __call__(self, scope, receive, send):
        if self._application is None:
            # Import Django and channels only when first called
            import django
            django.setup()

            from django.core.asgi import get_asgi_application
            from channels.routing import ProtocolTypeRouter, URLRouter
            from channels.auth import AuthMiddlewareStack
            import chat.routing

            self._application = ProtocolTypeRouter({
                "http": get_asgi_application(),
                "websocket": AuthMiddlewareStack(
                    URLRouter(
                        chat.routing.websocket_urlpatterns
                    )
                ),
            })
        await self._application(scope, receive, send)

application = ASGIApplication()
