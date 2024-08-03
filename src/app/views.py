from django.shortcuts import render

# Create your views here.

def top(request):
    return render(request, "app/top.html")

def index(request):
    return render(request, 'app/index.html')
