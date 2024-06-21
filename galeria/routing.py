#galeria\routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from galeria.consumers import ProgressConsumer

websocket_urlpatterns = [
    path("progress/<int:id_curso>/<str:checkbox_ia>/", ProgressConsumer.as_asgi()),
]


