from django.shortcuts import render
from django.http import HttpResponse
from .models import Memo
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

class MemoCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Memo
    fields = ['content', 'title', ]
    template_name = 'gpt/article_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class MemoUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Memo
    fields = ['content', 'title', ]
    template_name = 'gpt/article_form.html'

    # ほかのユーザから編集されないようにしてる
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if obj.author != self.request.user:
            raise PermissionDenied('You do not have permission to edit.')

        return super().dispatch(request, *args, **kwargs)

class MemoDeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = Memo
    success_url = reverse_lazy('gpt:index')
    template_name = 'gpt/article_confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if obj.author != self.request.user:
            raise PermissionDenied('You do not have permission to delete this.')

        return super().dispatch(request, *args, **kwargs)


class MemoListView(LoginRequiredMixin, generic.ListView):
    model = Memo
    template_name = 'gpt/article_list.html'

    def get_queryset(self):
        return Memo.objects.filter(author=self.request.user)

class MemoDetailView(LoginRequiredMixin, generic.DetailView):
    model = Memo
    template_name = 'gpt/article_detail.html'
    context_object_name = 'memo'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if obj.author != self.request.user:
            raise PermissionDenied('You do not have permission to view this.')

        return super().dispatch(request, *args, **kwargs)
