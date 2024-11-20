from django.db import models

from base.base import Base
from chat.models.chat import Chat


class Message(Base):
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('received', 'Received'),
        ('read', 'Read'),
    ]

    SENDER = [
        ('user', 'User'),
        ('restaurant', 'restaurant'),
    ]
    
    id = models.AutoField(primary_key=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')  
    sender = models.CharField(max_length=10, choices=SENDER,default='user')
    message = models.TextField() 
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='sent') 

    def __str__(self):
        return f"Message from {self.sender} at {self.created_at}..."  # Preview of the message
