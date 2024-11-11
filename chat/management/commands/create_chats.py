from django.core.management.base import BaseCommand
from chat.models.chat import Chat
import random

class Command(BaseCommand):
    help = "Create a specified number of Chat instances with random restaurant and client values"

    def add_arguments(self, parser):
        parser.add_argument('num_chats', type=int, help='Number of chats to create')

    def handle(self, *args, **kwargs):
        num_chats = kwargs['num_chats']
        
        # Sample List
        restaurants = ['Restaurant1', 'Restaurant2', 'Restaurant3', 'Restaurant4', 'Restaurant5']
        clients = ['ClientA', 'ClientB', 'ClientC', 'ClientD', 'ClientE']

        chats = [
            Chat(
                restaurant=random.choice(restaurants),
                client=random.choice(clients)
            )
            for _ in range(num_chats)
        ]
        
        Chat.objects.bulk_create(chats)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {num_chats} chats.'))
