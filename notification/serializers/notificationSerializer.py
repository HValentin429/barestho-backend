from rest_framework import serializers

from notification.models.notification import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'type', 'origin', 'read', 'sender', 'created_at']
