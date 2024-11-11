import time
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from chat.models import Message
import json

class ChatSSEView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        chat_id = self.kwargs['chat_id']
        response = HttpResponse(content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        response['Connection'] = 'keep-alive'
        
        def get_latest_message():
            latest_message = Message.objects.filter(chat_id=chat_id).order_by('-timestamp').first()
            if latest_message:
                return json.dumps({
                    'id': latest_message.id,
                    'content': latest_message.content,
                    'timestamp': latest_message.timestamp.isoformat(),
                })
            return None
        
        while True:
            latest_message = get_latest_message()
            if latest_message:
                response.write(f"data: {latest_message}\n\n")
                response.flush()
            time.sleep(1)
        
        return response
