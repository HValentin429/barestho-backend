import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

logger = logging.getLogger(__name__)

class NotificationStreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.notification_group_name = f'notifications_restaurant'

        await self.channel_layer.group_add(
            self.notification_group_name,
            self.channel_name
        )

        await self.accept()

    @database_sync_to_async
    def save_notification(self, user_id, notification_type, origin):
        from notification.models import Notification
        try:
            new_notification = Notification.objects.create(
                user_id=user_id,
                type=notification_type,
                origin=origin,
            )
            return new_notification
        except Exception as e:
            logger.error(f"Error saving notification: {e}")
            return None

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.notification_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        pass

    async def send_notification(self, notification):
        try:
            await self.send(text_data=json.dumps({
                'notification': notification,
            }))
        except Exception as e:
            logger.error(f"Error sending notification to WebSocket: {e}")
