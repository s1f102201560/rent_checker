import json
import uuid
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from django.template.loader import render_to_string

import fitz
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain_community.llms import OpenAI
from .models import Resource, ChatLog, ChatRoom

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room = await database_sync_to_async(ChatRoom.objects.get)(name=self.room_name)
        self.messages = []

        await self.accept()

        # 部屋名単位で存在確認し、存在しない場合のみ保存
        existing_log = await sync_to_async(ChatLog.objects.filter)(
            user=self.user, room=self.room
        )

        if not await sync_to_async(existing_log.exists)():
            await sync_to_async(ChatLog.objects.create)(
                user=self.user,
                room=self.room,
                prompt="",
                response=""
            )
            # サイドバー用の新しいログリンクを生成して送信
            sidebar_link_html = render_to_string(
                "app/_sidebar_link.html",
                {"log": {"room_name": self.room_name}},
            )
            await self.send(text_data=json.dumps({
                "type": "update_sidebar",
                "content": sidebar_link_html,
            }))


        # 非同期でデータベースクエリを実行
        resources = await sync_to_async(list)(Resource.objects.all())
        documents = []

        # OpenAIの埋め込みモデルを初期化
        embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY, base_url=settings.OPENAI_API_BASE)

        for resource in resources:
            pdf_path = resource.document.path
            text = ""
            with fitz.open(pdf_path) as pdf_doc:  # PDFを開く処理
                for page in pdf_doc:
                    text += page.get_text()
            documents.append(text)
            
            # テキストをベクトル化して保存
            embedding_vector = embeddings.embed_query(text)
            await sync_to_async(resource.update_embedding)(embedding_vector)

        # ベクトルを使ってFAISSのベクトルストアを作成
        vectorstore = FAISS.from_texts(documents, embeddings)

        # QAのプロンプトテンプレートを作成
        prompt_template = PromptTemplate(
            template="Use the following context to answer the question: {context}\nQuestion: {question}\nAnswer:",
            input_variables=["context", "question"]
        )

        # ドキュメントのチェインをロード
        combine_documents_chain = load_qa_chain(llm=OpenAI(openai_api_key=settings.OPENAI_API_KEY, base_url=settings.OPENAI_API_BASE), prompt=prompt_template)

        # RetrievalQAチェインを初期化
        self.qa_chain = RetrievalQA(
            retriever=vectorstore.as_retriever(),
            combine_documents_chain=combine_documents_chain
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_text = text_data_json["message"]

        # ユーザーメッセージをHTMLに変換して送信
        user_message_html = render_to_string(
            "app/chat_message.html",
            {"message_text": message_text, "is_system": False},
        )
        await self.send(text_data=user_message_html)
        self.messages.append({"role": "user", "content": message_text})

        # 空のシステムメッセージを表示
        message_id = f"message-{uuid.uuid4().hex}"
        system_message_html = render_to_string(
            "app/chat_message.html",
            {"message_text": "<i class='fas fa-spinner fa-spin'></i> ", "is_system": True, "message_id": message_id},
        )
        await self.send(text_data=system_message_html)

        # OpenAIを使って応答を生成
        response = await sync_to_async(self.qa_chain.run)(message_text)
        formatted_response = response.replace("\n", "<br>")

        # 応答をWebSocketで送信して、スピナーを応答で置き換える
        await self.send(text_data=f'<div id="{message_id}" hx-swap-oob="innerHTML">{formatted_response}</div>')

        self.messages.append({"role": "system", "content": response})

        # 対話ログを保存（部屋名も一緒に保存）
        await sync_to_async(ChatLog.objects.create)(
            user=self.user,
            room=self.room,
            prompt=message_text,
            response=response
        )