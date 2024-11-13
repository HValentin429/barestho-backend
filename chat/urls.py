from django.urls import path, include
from rest_framework.routers import DefaultRouter

from chat.views.messageView import MessageViewSet
from .views.chatView import ChatViewSet

router = DefaultRouter()
router.register(r'chats', ChatViewSet, basename='chat')
router.register(r'chat/(?P<chat_id>\d+)/messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]