from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import os

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
    return render(request, 'app/sandbox.html')

def sandbox_chat(request, room_name):
    if room_name is None:
        # ルーム名が指定されていない場合、部屋選択画面を表示
        return render(request, 'app/sandbox.html')
    else:
        # ルーム名が指定されている場合、そのルームに接続する
        context = {'room_name': room_name}
        return render(request, 'app/sandbox_chat.html', context)

@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        file = request.FILES['file']
        file_name = file.name
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        # 画像のURLを返す
        image_url = request.build_absolute_uri(settings.MEDIA_URL + file_name)
        return JsonResponse({'image_url': image_url})
    return JsonResponse({'error': 'Invalid request'}, status=400)