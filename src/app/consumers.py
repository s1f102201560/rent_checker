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

            # Call GPT-4 API
            response_message = await self.get_gpt_response(image_url)
            await self.send(text_data=json.dumps({"message": response_message}))

    async def get_gpt_response(self, image_url):
        response = await asyncio.get_event_loop().run_in_executor(None, self.call_openai_api, image_url)
        return response

    def call_openai_api(self, image_url):
        
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
            ]
        )
        explanation_markdown = response.choices[0].message.content
        return explanation_markdown
