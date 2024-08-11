from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    # re_path(r"ws/index/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
    re_path(r"ws/sandbox_chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi(), name="sandbox_chat_ws"),

]