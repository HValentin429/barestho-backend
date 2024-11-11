from django.db import models

class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    restaurant = models.CharField(max_length=100, default='')
    client = models.CharField(max_length=100, default='')

    def __str__(self):
        return f"Chat {self.id} between {self.client} and {self.restaurant}"