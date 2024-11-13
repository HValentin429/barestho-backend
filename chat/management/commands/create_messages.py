from django.core.management.base import BaseCommand
from chat.models import Message, Chat
import random

class Command(BaseCommand):
    help = "Create a conversation with sample messages for a specific chat ID"

    def add_arguments(self, parser):
        parser.add_argument('chat_id', type=int, help='ID of the chat to associate the messages')

    def handle(self, *args, **kwargs):
        chat_id = kwargs['chat_id']

        try:
            chat = Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Chat with ID {chat_id} does not exist.'))
            return

        senders = ['user', 'Restaurant']
        sample_messages = [
            "Hello, I have a question about your menu.",
            "Can I make a reservation for two?",
            "What are your operating hours?",
            "Can I order takeout?",
            "Do you offer vegetarian options?"
        ]
        messages = [
            Message(
                chat=chat, 
                sender=random.choice(senders), 
                message=random.choice(sample_messages)  
            )
            for _ in range(5)  
        ]


        Message.objects.bulk_create(messages)

        self.stdout.write(self.style.SUCCESS(f'Successfully created a conversation with 5 sample messages for chat ID {chat_id}.'))
