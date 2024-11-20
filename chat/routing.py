from django.urls import re_path
from chat.views.messageViewSSE import MessageStreamConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<chat_id>\d+)/messages/stream$', MessageStreamConsumer.as_asgi()),
]