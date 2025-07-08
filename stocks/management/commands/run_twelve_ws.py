import asyncio
import json
import websockets
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.management.base import BaseCommand
from django.conf import settings
import re

API_KEY = settings.TWELVE_DATA_API_KEY

POPULAR_TICKERS = ["EUR/USD", "BTC/USD"]

async def connect_to_twelve_data():
    uri = f"wss://ws.twelvedata.com/v1/quotes/price?apikey={API_KEY}"
    channel_layer = get_channel_layer()

    try:
        async with websockets.connect(uri) as websocket:
            # Send subscription message
            subscribe_message = {
                "action": "subscribe",
                "params": {
                    "symbols": ",".join(POPULAR_TICKERS)
                }
            }
            await websocket.send(json.dumps(subscribe_message))
            print("✅ Sent subscription request:", subscribe_message)

            # Wait for confirmation
            response = await websocket.recv()
            print("🧾 Subscription response from Twelve Data:", response)

            # Give frontend time to join groups
            await asyncio.sleep(5)

            # Start receiving price updates
            while True:
                try:
                    message = await websocket.recv()
                    data = json.loads(message)

                    if "symbol" in data and "price" in data:
                        ticker = data["symbol"]
                        price = float(data["price"])

                        print(f"📈 Received price for {ticker}: {price}")

                        safe_symbol = re.sub(r'[^a-zA-Z0-9._-]', '_', ticker.upper())
                        group_name = f"stock_{ticker.lower().replace('/', '-')}"

                        payload = {
                            "current": price,
                            "change": 0.00,
                            "percent_change": 0.00
                        }

                        await channel_layer.group_send(
                            group_name,
                            {
                                "type": "send_stock_update",
                                "data": payload
                            }
                        )

                        print(f"📢 Sent to group {group_name}: {payload}")

                except json.JSONDecodeError:
                    print("⚠️ Failed to decode message:", message)
                except Exception as e:
                    print("⚠️ Error receiving message:", e)
                    await asyncio.sleep(1)

    except Exception as e:
        print("❌ Connection error:", e)
        await asyncio.sleep(5)
        await connect_to_twelve_data()  # Reconnect

def run():
    asyncio.run(connect_to_twelve_data())

class Command(BaseCommand):
    help = 'Run Twelve Data WebSocket integration'

    def handle(self, *args, **kwargs):
        run()
