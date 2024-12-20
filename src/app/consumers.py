import json
import uuid
from asgiref.sync import sync_to_async
from config import settings
from channels.generic.websocket import AsyncWebsocketConsumer
from django.template.loader import render_to_string
from asgiref.sync import sync_to_async
from config import settings
from .rag_initializer import initialize_rag_chain
from .vectorstore_initializer import initialize_vectorstore
from .models import ChatLog, ChatRoom
import pprint

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # ユーザー情報とセッションIDを設定
        self.user = self.scope["user"]
        # FIXME localでしか動作しないハードコードをしている
        self.room_name = settings.BASE_URL + self.scope["url_route"]["kwargs"]["room_name"]
        self.session_id = f"{self.user.id}-{self.room_name}"
        self.room = await sync_to_async(ChatRoom.objects.get)(link=self.room_name)

        # Retrieverを初期化
        self.retriever = await initialize_vectorstore()
        
        # RAGチェーンの初期化
        self.rag_chain, self.get_session_history = initialize_rag_chain(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_API_BASE,
            model_name=settings.OPENAI_MODEL,
            retriever=self.retriever
        )

        await self.accept()

    async def receive(self, text_data):
        # クライアントからのメッセージを取得
        text_data_json = json.loads(text_data)
        message_text = text_data_json.get("message", "")

        # ユーザーメッセージ用のIDを生成
        user_message_id = f"user-{uuid.uuid4().hex}"
        user_message_html = render_to_string(
            "app/chat/message.html",
            {
                "message_text": message_text,
                "is_system": False,
                "message_id": user_message_id,
            },
        )
        await self.send(text_data=json.dumps({"message_id": user_message_id, "message_text": user_message_html}))

        # スピナーを表示するためのIDを生成
        system_message_id = f"system-{uuid.uuid4().hex}"
        spinner_html = render_to_string(
            "app/chat/message.html",
            {
                "message_text": "<i class='fas fa-spinner fa-spin'></i>",
                "is_system": True,
                "message_id": system_message_id,
            },
        )

        await self.send(text_data=json.dumps({"message_id": system_message_id, "message_text": spinner_html}))

        try:
            # 質問をRAGチェーンに渡して応答を生成
            result = await sync_to_async(self.rag_chain.invoke)(
                {"input": message_text},
                {"configurable": {"session_id": self.session_id}}
            )
            answer = result["answer"]

            response_html = render_to_string(
                "app/chat/message.html",
                {
                    "message_text": answer,
                    "is_system": True,
                    "message_id": system_message_id},
            )
            await self.send(text_data=json.dumps({"message_id": system_message_id, "message_text": response_html}))

            # 会話ログをデータベースに保存
            await sync_to_async(ChatLog.objects.create)(
                user=self.user, room=self.room, prompt=message_text, response=answer
            )
        except Exception as e:
            print(f"Error processing query: {e}")
            error_html = render_to_string(
                "app/chat/message.html",
                {"message_text": "エラーが発生しました。もう一度お試しください。", "is_system": True},
            )
            await self.send(text_data=json.dumps({"message_id": system_message_id, "message_text": error_html}))
