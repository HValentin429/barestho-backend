from django.urls import re_path

from notification.views.notificationViewSSE import NotificationStreamConsumer

websocket_urlpatterns = [
    re_path(r'ws/notifications/$', NotificationStreamConsumer.as_asgi()),
]