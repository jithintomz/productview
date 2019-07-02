from django.conf.urls import url
from channels.routing import URLRouter
from channels.http import AsgiHandler
from channels.auth import AuthMiddlewareStack
from django.urls import path

from productview import consumers

urlpatterns = [
    url(r'', AsgiHandler),
]

websocket_urlpatterns = [
    path('ws/messages/<int:upload_id>/', consumers.ChatConsumer),
]