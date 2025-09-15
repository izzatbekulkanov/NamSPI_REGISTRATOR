import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({
            "message": "WebSocket ulanish muvaffaqiyatli amalga oshdi ✅"
        }))

    async def disconnect(self, close_code):
        print("WebSocket uzildi")

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            data = json.loads(text_data)
            message = data.get("message", "")
            await self.send(text_data=json.dumps({
                "message": f"Siz yubordingiz: {message}"
            }))
