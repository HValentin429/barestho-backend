from django.contrib import admin
from django.urls import include, path, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chat.urls')),
    path('api/', include('notification.urls')),
]