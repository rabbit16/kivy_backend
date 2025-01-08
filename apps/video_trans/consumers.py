import json

from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """这里要管理链接，用来维持视频信号"""
        print("hello")
        # 接受来自Websocket的连接
        self.video_name = self.scope["url_route"]["kwargs"]["group"]
        self.room_group_name = self.video_name

        await self.channel_layer.group_add(self.room_group_name,
                                           self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # 连接正在关闭的时候，删除前后端之间的通道
        await self.channel_layer.group_discard(self.room_group_name,
                                               self.channel_name)
    def format_send_data(self, json_data):
        raw_message = {
            "headers": {
                "type": "system",
                "message": "receive",
                "author": "server",
                "receiver": json_data["headers"]["author"],
            },
            "body": {

            }
        }
    async def receive(self, text_data=None, bytes_data=None):
        # print(text_data)
        json_data = json.loads(text_data)
        source = json_data["headers"]["type"]
        message = json_data["headers"]["message"]
        if message == "ping":
            json_data["headers"]["message"] = "receive"
            receiver = json_data["headers"]["author"]
            json_data["headers"]["author"] = "server"
            json_data["headers"]["receiver"] = receiver
        elif message == "require_send":
            json_data["headers"]["message"] = "require_send"
            receiver = json_data["headers"]["author"]
            json_data["headers"]["author"] = "server"
            json_data["headers"]["receiver"] = receiver
        if message == "require_send":
            await self.channel_layer.group_send(
                "system",
                {
                    "type": "chat_message",
                    "message": json_data
                }
            )
        else:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": json_data
                }
            )


    async def chat_message(self, event):
        # print(event)
        await self.send(text_data=json.dumps(event["message"]))

    async def heartbeat_message(self, event):
        if self.websocket_connect:
            try:
                await self.send("--pong--")
            except Exception as e:
                # 连接已断开
                print(e)
                pass