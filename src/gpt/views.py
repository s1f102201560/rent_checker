from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views import generic
from .models import Memo
from .forms import MemoForm
import os
from django.http import HttpResponseForbidden
from django.conf import settings
from django.http import HttpResponse, Http404

base_url = "https://api.openai.iniad.org/api/v1"
api_key = os.getenv('OPENAI_API_KEY')

# アップロードしたファイルをほかのユーザーから見れなくするコード
# configの方にurlがある
def protected_media(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', path)
    memo = get_object_or_404(Memo, file='uploads/' + path)
    
    if memo.author != request.user:
        return HttpResponseForbidden("You do not have permission to access this file.")

    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type="application/octet-stream")
        response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
        return response


class MemoCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Memo
    form_class = MemoForm
    template_name = 'gpt/article_form.html'

    # ほかのユーザーから編集、削除されないようにしている
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class MemoUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Memo
    form_class = MemoForm
    template_name = 'gpt/article_form.html'

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        memo = self.get_object()
        file_extension = memo.file.name.split('.')[-1].lower()
        context['is_image'] = file_extension in ['png', 'jpg', 'jpeg']
        return context
