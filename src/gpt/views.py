from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from .models import Article, Board

class BoardListView(LoginRequiredMixin, generic.ListView):
    model = Board
    template_name = 'gpt/board_list.html'

    def get_queryset(self):
        return Board.objects.filter(user=self.request.user)

class ArticleListView(LoginRequiredMixin, generic.ListView):
    model = Article
    template_name = 'gpt/article_list.html'

    def get_queryset(self):
        board = get_object_or_404(Board, id=self.kwargs['board_id'], user=self.request.user)
        return Article.objects.filter(board=board)

class ArticleCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Article
    fields = ['title', 'content']
    template_name = 'gpt/article_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.board = get_object_or_404(Board, id=self.kwargs['board_id'], user=self.request.user)
        return super().form_valid(form)

class ArticleUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Article
    fields = ['title', 'content']
    template_name = 'gpt/article_form.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied('You do not have permission to edit.')
        return super().dispatch(request, *args, **kwargs)

class ArticleDeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = Article

    def get_success_url(self):
        return reverse_lazy('gpt:article_list', kwargs={'board_id': self.object.board.id})

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied('You do not have permission to delete.')
        return super().dispatch(request, *args, **kwargs)

class ArticleDetailView(LoginRequiredMixin, generic.DetailView):
    model = Article
    template_name = 'gpt/article_detail.html'
