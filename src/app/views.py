from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import ChatLog
import os
import openai

def top(request):
    return render(request, "app/top.html")

def index(request):
    return render(request, 'app/index.html')

def sandbox(request):
    return render(request, 'app/sandbox.html')

def sandbox_chat(request, room_name):
    logs = ChatLog.objects.filter(room_name=room_name, user=request.user)
    return render(request, 'app/sandbox_chat.html', {
        'room_name': room_name,
        'chat_logs': logs
    })

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