#galeria\routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from galeria.consumers import ProgressConsumer
from galeria.consumers_class_prof import UpdateConsumerClassProf

websocket_urlpatterns = [
    path("progress/<int:id_curso>/<str:checkbox_ia>/", ProgressConsumer.as_asgi()),
    path('ws/update_class_prof/', UpdateConsumerClassProf.as_asgi()),
]


