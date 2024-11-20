import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
import re

logger = logging.getLogger(__name__)

class MessageStreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_name = f'chat_{self.chat_id}'

        await self.channel_layer.group_add(
            self.chat_name,
            self.channel_name
        )

        await self.accept()

    @database_sync_to_async
    def save_message(self, chat_id, message, sender):
        from chat.models import Message
        try:
            new_message = Message.objects.create(chat_id=chat_id, message=message, sender=sender)
            return new_message
        except Exception as e:
            logger.error(f"Error saving message: {e}")
            return None

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json.get('message')
            sender = text_data_json.get('sender')

            if message:
                new_message = await self.save_message(self.chat_id, message, sender)

                if new_message:
                    
                    await self.channel_layer.group_send(
                        self.chat_name,
                        {
                            'type': 'send.message',
                            'message': {
                                'id': new_message.id,
                                'chat_id': new_message.chat_id,
                                'message': new_message.message,
                                'created_at': new_message.created_at.isoformat(),
                                'sender': new_message.sender,
                            },
                        }
                    )

        except Exception as e:
            logger.error(f"Error processing received message: {e}")

    async def send_message(self, event):
        try:
            message = event['message']
            await self.send(text_data=json.dumps({
                'message': message,
            }))
        except Exception as e:
            logger.error(f"Error sending message to WebSocket: {e}")