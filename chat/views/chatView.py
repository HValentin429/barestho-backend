from rest_framework import viewsets
from django.db.models import OuterRef, Subquery
from chat.models import Chat, Message
from chat.serializers.chatSerializer import ChatSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework import status

def get_chats():
    latest_message = Message.objects.filter(chat=OuterRef('pk')).order_by('-created_at')
    chats = Chat.objects.annotate(
        last_message_id=Subquery(latest_message.values('id')[:1]),
        latest_message_time=Subquery(latest_message.values('created_at')[:1]),
    ).order_by('-latest_message_time')
    
    return chats

from rest_framework.response import Response

class ChatViewSet(viewsets.ModelViewSet):
    serializer_class = ChatSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ['client']

    def get_queryset(self):
        return get_chats()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(latest_message_time__isnull=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data) 
    
    @action(detail=False, methods=['get'], url_path='')
    def get_chat_by_id(self, request, *args, **kwargs):
        chat_id = request.query_params.get('idChat')

        if not chat_id:
            return Response({"detail": "idChat parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            chat = get_chats().get(id=chat_id)
        except Chat.DoesNotExist:
            return Response({"detail": "Chat not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(chat)
        return Response(serializer.data)