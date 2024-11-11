from rest_framework import serializers
from chat.models import Chat, Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'message', 'timestamp', 'sender', 'status']

class ChatSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ['id', 'client', 'restaurant', 'last_message']

    def get_last_message(self, obj):
        if obj.last_message_id:
            return MessageSerializer(Message.objects.get(id=obj.last_message_id)).data
        return None
