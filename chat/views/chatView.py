from rest_framework import viewsets
from django.db.models import OuterRef, Subquery
from chat.models import Chat, Message
from chat.serializers.chatSerializer import ChatSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

def get_chats():
    latest_message = Message.objects.filter(chat=OuterRef('pk')).order_by('-timestamp')
    
    chats = Chat.objects.all().annotate(
        last_message_id=Subquery(latest_message.values('id')[:1]), 
    )

    return chats

class ChatViewSet(viewsets.ModelViewSet):
    serializer_class = ChatSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ['client__name']

    def get_queryset(self):
        return get_chats()
