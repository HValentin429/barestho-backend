from datetime import datetime
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.db.models import OuterRef, Subquery

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from notification.models.notification import Notification
from notification.serializers.notificationSerializer import NotificationSerializer

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import logging

logger = logging.getLogger(__name__)


def create_and_send_notification(notification_type, origin, sender):
    try:
        Notification.objects.filter(type=notification_type, origin=origin, read=False).update(read=True)

        created_at_value = datetime.now().isoformat()
        new_notification = Notification.objects.create(
            type=notification_type,
            origin=origin,
            sender=sender,
            read=False,
            created_at=created_at_value 
        )

        notification_data = {
                'type': new_notification.type,
                'origin': new_notification.origin,
                'sender': new_notification.sender,
                'created_at': created_at_value
        }

        channel_layer = get_channel_layer()
        group_name = f'notifications_restaurant'
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'send.notification',
                'message': notification_data
            }
        )

    except Exception as e:
        logger.error(f"Error creating and sending notification: {e}")

def get_notifications():
    notifications = Notification.objects.all().filter(read=False)
    return notifications

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ['origin', 'type']

    def get_queryset(self):
        return get_notifications()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['patch'], url_path='mark-as-read')
    def mark_as_read(self, request, *args, **kwargs):
        notification_id = request.query_params.get('idNotification')

        if not notification_id:
            return Response({"detail": "idNotification parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
        
            notification = Notification.objects.get(id=notification_id)
            notification.read = True 
            notification.save()

            return Response({"detail": "Notification marked as read."}, status=status.HTTP_200_OK)

        except Notification.DoesNotExist:
            return Response({"detail": "Notification not found."}, status=status.HTTP_404_NOT_FOUND)
