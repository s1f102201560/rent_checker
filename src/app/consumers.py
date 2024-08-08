import json
import openai
import asyncio
from django.conf import settings
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        if 'message' in text_data_json:
            message = text_data_json["message"]
            await self.send(text_data=json.dumps({"message": message}))

        if 'image_url' in text_data_json:
            image_url = text_data_json['image_url']

            # Call GPT-4o API
            await self.send(text_data=json.dumps({"message": "Processing image..."}))
            await self.get_gpt_response(image_url)

    async def get_gpt_response(self, image_url):
        await asyncio.get_event_loop().run_in_executor(None, self.call_openai_api, image_url)

    def call_openai_api(self, image_url):
        openai.api_key = settings.OPENAI_API_KEY
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY, base_url="https://api.openai.iniad.org/api/v1")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": "次の画像は賃貸契約の見積書です。余計なコストがかかっているところやアドバイスをしてください"
                },
                {
                    "role": "system",
                    "content": image_url
                }
            ],
            stream=True,
        )

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def send_chunks():
            buffer = ""
            for chunk in response:
                if hasattr(chunk.choices[0], 'delta') and hasattr(chunk.choices[0].delta, 'content'):
                    content = chunk.choices[0].delta.content
                    if content:
                        buffer += content
                        if "。" in buffer or "、" in buffer:
                            parts = buffer.split("。")
                            for part in parts[:-1]:
                                await self.send_to_client(part.strip() + "。")
                            buffer = parts[-1]

                        await asyncio.sleep(0.1)  # Add a slight delay to slow down the streaming

            # Send any remaining content in the buffer
            if buffer:
                await self.send_to_client(buffer.strip())

        loop.run_until_complete(send_chunks())

    async def send_to_client(self, content):
        await self.send(text_data=json.dumps({"message": content}))
