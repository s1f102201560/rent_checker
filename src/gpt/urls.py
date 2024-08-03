from django.urls import path
from . import views

app_name = 'gpt'

urlpatterns = [
    path('', views.BoardListView.as_view(), name='board_list'),
    path('board/<int:board_id>/', views.ArticleListView.as_view(), name='article_list'),
    path('board/<int:board_id>/create/', views.ArticleCreateView.as_view(), name='article_create'),
    path('article/<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('article/<int:pk>/edit/', views.ArticleUpdateView.as_view(), name='article_edit'),
    path('article/<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='article_delete'),
]
