from django.db import models

from base.base import Base

class Notification(Base):

    TYPE = [
        ('message', 'message'),
        ('chat', 'chat'),
    ]

    id = models.AutoField(primary_key=True)
    type= models.CharField(max_length=30, choices=TYPE, default='new_message')
    #in real use case, it would be an ID
    sender = models.CharField(max_length=100, default='')
    origin = models.CharField(max_length=100, default='')
    read = models.BooleanField(default=False)
    

    def __str__(self):
        return f"Notification {self.id} of type {self.type} from {self.origin}"