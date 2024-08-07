from django.urls import path
from . import views
from .models import Memo

app_name = 'gpt'

urlpatterns = [
    path('', views.MemoListView.as_view(), name='index'),
    path('<int:pk>/', views.MemoDetailView.as_view(), name='detail'),
    path('create/', views.MemoCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.MemoUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.MemoDeleteView.as_view(), name='delete'),
]
