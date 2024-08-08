from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
# from langchain import hub
# from langchain_chroma import Chroma
# from langchain_community.document_loaders import WebBaseLoader
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnablePassthrough
# from langchain_openai import OpenAIEmbeddings, ChatOpenAI
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# import bs4
import openai

def top(request):
    return render(request, "app/top.html")

def index(request):
    return render(request, 'app/index.html')

openai.api_key = settings.OPENAI_API_KEY
openai.api_base = settings.OPENAI_API_BASE

def send_direct_openai_request(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ],
            max_tokens=150
        )
        return response
    except Exception as e:
        print(f"Direct OpenAI API error: {e}")
        return None

def sandbox(request):
    print("Received request")  # デバッグ用
    if request.method == 'POST':
        print("POST request received")  # デバッグ用
        question = request.POST.get('question')
        print(f"Question received: {question}")  # デバッグ用
        try:
            response = send_direct_openai_request(question)
            if response:
                print(f"Question: {question}, Response: {response}")  # デバッグ用
                return JsonResponse({'response': response['choices'][0]['message']['content']})
            else:
                return JsonResponse({'error': 'OpenAI API request failed'}, status=500)
        except Exception as e:
            print(f"Error: {e}")  # デバッグ用
            return JsonResponse({'error': str(e)}, status=500)
    print("Rendering sandbox.html")  # デバッグ用
    return render(request, 'app/sandbox.html')

def sandbox_room(request, room_name):
    return render(request, "app/sandbox_room.html", {"room_name": room_name})