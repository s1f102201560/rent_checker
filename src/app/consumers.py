import json
import uuid
import pytesseract
from PIL import Image
import base64
import io
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
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from .models import Resource, ChatLog, ChatRoom

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room = await database_sync_to_async(ChatRoom.objects.get)(name=self.room_name)
        self.messages = []

        await self.accept()

        # 非同期でデータベースクエリを実行
        resources = await sync_to_async(list)(Resource.objects.all())
        documents = []

        #OpenAIモデルを初期化
        llm = OpenAI(openai_api_key=settings.OPENAI_API_KEY, base_url=settings.OPENAI_API_BASE)
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
            #template="Use the following context to answer the question: {context}\nQuestion: {question}\nAnswer:",
            template = (
            "あなたは賃貸物件を探している人の手助けになるAIです。"
            "以下のコンテキストと会話履歴を使用して、適切な内容をユーザーに提供してください。\n"
            "コンテキスト: {context}\n"
            "会話履歴: {chat_history}\n"
            "質問: {question}\n"
            "回答:"
            ),
            input_variables=["context", "chat_history", "question"]
        )

        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            input_key="question"
        )

        # ドキュメントのチェインをロード
        combine_documents_chain = load_qa_chain(
            llm=llm,
            prompt=prompt_template
        )
        # RetrievalQAチェインを初期化
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(),
            memory=self.memory
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_text = text_data_json.get("message", "")
        image_data = text_data_json.get("image", "")

        # ユーザーメッセージをHTMLに変換して送信
        user_message_html = render_to_string(
            "app/chat_message.html",
            {"message_text": message_text, "is_system": False},
        )
        await self.send(text_data=json.dumps({
            "message_text": user_message_html
        }))

        self.messages.append({"role": "user", "content": message_text})

        # 空のシステムメッセージを表示
        message_id = f"message-{uuid.uuid4().hex}"
        system_message_html = render_to_string(
            "app/chat_message.html",
            {
                "message_text": "<i class='fas fa-spinner fa-spin'></i>",
                "is_system": True,
                "message_id": message_id
            }
        )
        await self.send(text_data=json.dumps({
            "message_id": message_id,
            "message_text": system_message_html
        }))

        # 画像が送信された場合、OCRで画像からテキストを抽出
        if image_data:            
            try:
                # Base64デコード
                decoded_image_data = base64.b64decode(image_data)
                # 画像を開く
                image = Image.open(io.BytesIO(decoded_image_data))
                image.verify()
                image = Image.open(io.BytesIO(decoded_image_data))
                # OCRでテキストを抽出
                ocr_text = pytesseract.image_to_string(image, lang="jpn")

                print(ocr_text)
                # GPTに投げるメッセージとして、抽出したテキストを含める
                message_text += f"\n[画像から抽出されたテキスト]\n{ocr_text}"
            except Exception as e:
                print(f"Error loading image; {e}")
                return
        try:
            # OpenAIを使って応答を生成
            response = await sync_to_async(self.qa_chain)({"question": message_text})

            answer = response["answer"]

            # 応答メッセージを同じmessage_idで送信
            response_html = render_to_string(
                "app/chat_message.html",
                {
                    "message_text": answer,
                    "is_system": True,
                    "message_id": message_id,  # スピナーと同じmessage_idを使用
                }
            )

            # WebSocketでスピナーを応答に置き換える
            await self.send(text_data=json.dumps({
                "message_id": message_id,
                "message_text": response_html
            }))

            self.messages.append({"role": "system", "content": answer})

            # 対話ログを保存（部屋名も一緒に保存）
            await sync_to_async(ChatLog.objects.create)(
                user=self.user,
                room=self.room,
                prompt=message_text,
                response=answer
            )
        except Exception as e:
            print(f"Error processing GPT query: {e}")

