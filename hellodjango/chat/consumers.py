import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope["url_route"]["kwargs"]["session_id"]
        self.group_name = f"chat_{self.session_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def chat_message(self, event):
        message = event["message"]   # <- 重点

        await self.send(text_data=json.dumps({
            "role": message["role"],
            "content": message["content"],
            "created_at": message.get("created_at")
        }))