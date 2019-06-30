from django.conf.urls import url
from channels.routing import URLRouter
from channels.http import AsgiHandler
from channels.auth import AuthMiddlewareStack
import django_eventstream
from django.urls import path

from productview import consumers

urlpatterns = [
    url(r'^events/', AuthMiddlewareStack(
        URLRouter(django_eventstream.routing.urlpatterns)
    ), {'channels': ['test']}),
    url(r'', AsgiHandler),
]

websocket_urlpatterns = [
    path('ws/messages/<int:upload_id>/', consumers.ChatConsumer),
]