# asgi.py
import os
from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barestho_backend.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(), 
    "websocket": URLRouter(          
        chat.routing.websocket_urlpatterns 
    ),
})