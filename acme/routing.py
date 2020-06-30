from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import productview.routing


application = ProtocolTypeRouter({
    'http': URLRouter(productview.routing.urlpatterns),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            productview.routing.websocket_urlpatterns
        )
    ),
})
