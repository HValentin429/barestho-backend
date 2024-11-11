from django.db import models

from chat.models.chat import Chat
from user.models.user import User

class Message(models.Model):
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('received', 'Received'),
        ('read', 'Read'),
    ]

    SENDER = [
        ('user', 'User'),
        ('Restaurant', 'Restaurant'),
    ]
    
    id = models.AutoField(primary_key=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')  
    sender = models.CharField(max_length=10, choices=SENDER,default='user')
    message = models.TextField() 
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='sent') 
    timestamp = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Message from {self.sender} at {self.timestamp}: {self.message[:30]}..."  # Preview of the message
