import os
import fitz  # PyMuPDF
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from django.conf import settings
from asgiref.sync import sync_to_async
from .models import Resource

async def initialize_vectorstore():
    """
    PDFを読み込み、VectorStoreとRetrieverを初期化します。

    Returns:
        retriever: FAISSベースのRetriever
    """
    # OpenAI埋め込みモデルの初期化
    embeddings = OpenAIEmbeddings(
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_API_BASE,
        model="text-embedding-ada-002",
    )

    # データベースからリソースを取得
    resources = await sync_to_async(list)(Resource.objects.all())

    # PDFからテキストを抽出し、VectorStoreに格納
    documents = []
    for resource in resources:
        pdf_path = resource.document.path
        text = ""
        with fitz.open(pdf_path) as pdf_doc:  # PDFを開く
            for page in pdf_doc:
                text += page.get_text()
        documents.append(text)

        # 各リソースのベクトルを生成して保存
        embedding_vector = embeddings.embed_query(text)
        await sync_to_async(resource.update_embedding)(embedding_vector)

    # FAISS VectorStoreの初期化
    vectorstore = FAISS.from_texts(documents, embeddings)

    # Retrieverを作成
    retriever = vectorstore.as_retriever()
    return retriever
