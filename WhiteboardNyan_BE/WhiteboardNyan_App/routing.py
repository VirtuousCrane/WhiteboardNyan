from WhiteboardNyan_BE.WhiteboardNyan_App.consumers import WhiteboardConsumer
from django.conf.urls import url

websocket_urlpatterns = [
    url(r'^ws/whiteboard/(?P<room_code>\w+)/$', WhiteboardConsumer.as_asgi()),
]
