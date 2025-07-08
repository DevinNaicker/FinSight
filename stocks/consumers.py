import json
from channels.generic.websocket import AsyncWebsocketConsumer
import re


class StockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        symbol = self.scope['url_route']['kwargs']['symbol']
        self.group_name = f"stock_{symbol.lower()}"  # must match run_twelve_ws.py

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        print(f"✅ Connected to group: {self.group_name}")
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        print(f"❌ Disconnected from group: {self.group_name}")

    async def receive(self, text_data):
        print("📥 Received from frontend (ignored):", text_data)

    async def send_stock_update(self, event):
        print(f"📤 Sending update to frontend: {event['data']}")
        await self.send(text_data=json.dumps(event["data"]))


class TestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({
            "message": "WebSocket connected and working 🎉"
        }))
        print("✅ TestConsumer connection accepted")

    async def disconnect(self, close_code):
        print("❌ TestConsumer disconnected")

    async def receive(self, text_data):
        print("📥 TestConsumer received:", text_data)
        data = json.loads(text_data)
        await self.send(text_data=json.dumps({
            "response": f"Received: {data.get('message')}"
        }))