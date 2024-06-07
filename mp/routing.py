from django.urls import path

from mp.views import SSEView

websocket_urlpatterns = [
    path('sse_endpoint/', SSEView.as_asgi(), name='SSEView')
]
