from django.urls import re_path
from queueing.consumers import QueueConsumer

websocket_urlpatterns = [
    re_path(r"ws/queue_updates/$", QueueConsumer.as_asgi()),
]
