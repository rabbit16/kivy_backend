from django.urls import re_path
from apps.video_trans import consumers
# 示例路由
websocket_urlpatterns = [
    re_path(r'ws/(?P<group>\w+)/$', consumers.ChatConsumer.as_asgi())]