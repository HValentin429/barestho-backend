import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import Message

class MessageStreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f'chat_{self.chat_id}'
        await self.accept()
        self.last_seen_id = None
        await self.send_initial_messages()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        if message:
            Message.objects.create(chat_id=self.chat_id, message=message)
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def send_initial_messages(self):
        while True:
            new_messages = Message.objects.filter(chat_id=self.chat_id, id__gt=self.last_seen_id).order_by('created_at')
            if new_messages.exists():
                for message in new_messages:
                    self.last_seen_id = message.id
                    await self.send(text_data=json.dumps({
                        'message': message.message
                    }))
            await asyncio.sleep(1)
