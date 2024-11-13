from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from chat.models import Message

from rest_framework import status
from chat.serializers.chatSerializer import MessageSerializer

class MessageViewSet(viewsets.ViewSet):    
    def list(self, request, chat_id=None):
        if chat_id:
            messages = Message.objects.filter(chat_id=chat_id).order_by('created_at')
        else:
            messages = Message.objects.all().order_by('created_at')
        
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def create(self, request, chat_id=None):
        data = request.data
        data['chat'] = chat_id 
        
        serializer = MessageSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
