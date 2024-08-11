import json
import uuid
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from django.template.loader import render_to_string

import fitz
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain_community.llms import OpenAI
from asgiref.sync import sync_to_async
from .models import Resource

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.messages = []
        await super().connect()

        # 非同期でデータベースクエリを実行
        resources = await sync_to_async(list)(Resource.objects.all())
        documents = []

        # OpenAIの埋め込みモデルを初期化
        embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY, base_url=settings.OPENAI_API_BASE)

        for resource in resources:
            pdf_path = resource.document.path
            text = ""
            with fitz.open(pdf_path) as pdf_doc:
                for page in pdf_doc:
                    text += page.get_text()
            documents.append(text)
            
            # テキストをベクトル化して保存
            embedding_vector = embeddings.embed_query(text)  # 修正されたメソッド名
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

        user_message_html = render_to_string(
            "app/sandbox_chat_message.html",
            {"message_text": message_text, "is_system": False},
        )
        await self.send(text_data=user_message_html)
        self.messages.append({"role": "user", "content": message_text})

        message_id = f"message-{uuid.uuid4().hex}"
        system_message_html = render_to_string(
            "app/sandbox_chat_message.html",
            {"message_text": "", "is_system": True, "message_id": message_id},
        )
        await self.send(text_data=system_message_html)

        response = self.qa_chain.run(message_text)
        formatted_response = response.replace("\n", "<br>")
        await self.send(text_data=f'<div id="{message_id}" hx-swap-oob="beforeend">{formatted_response}</div>')

        self.messages.append({"role": "system", "content": response})
