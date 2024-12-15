from langchain.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import ChatMessageHistory

# RAGチェーンの初期化関数
def initialize_rag_chain(api_key, base_url, model_name, retriever):
    # OpenAI LLMモデルの初期化
    llm = ChatOpenAI(
        api_key=api_key,
        base_url=base_url,
        model_name=model_name,
        temperature=0.7,
    )

    # 質問の文脈化プロンプト
    contextualize_q_system_prompt = """チャット履歴と最新のユーザー質問が与えられます。最新の質問はチャット履歴のコンテキストを参照している可能性があります。チャット履歴を参照せずに理解できるように、スタンドアロンの質問を作成してください。質問を再構成する必要がない場合は、そのまま返してください。回答はしないでください。"""
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    # 履歴対応リトリーバー
    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)

    # 質問応答プロンプト
    qa_system_prompt = """あなたは賃貸仲介の専門家です。以下の取得したコンテキストを使用して質問に答えてください。コンテキストが関連していない場合は、あなた自身の知識を使用して質問に答えてください。答えは日本語で、3文以内で簡潔にしてください。

    {context}
    """
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    # 質問応答用チェーンの作成
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    # グローバルストアでセッションごとのチャット履歴を管理
    store = {}

    def get_session_history(session_id):
        if session_id not in store:
            store[session_id] = ChatMessageHistory()
        return store[session_id]

    # 会話履歴付きRAGチェーン
    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )

    return conversational_rag_chain, get_session_history
