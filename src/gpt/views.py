from django.shortcuts import render
from django.http import HttpResponse
from .models import Article
from django.views import generic

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

class CreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Article
    fields = ['content', 'title', ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreateView, self).form_valid(form)

def index(request):
    return HttpResponse('Hello Django')

def detail(request, id):
    return HttpResponse('detail ' + str(id))

def create(request):
    return HttpResponse('create')

class UpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Article
    fields = ['content', 'title', ]
 
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
 
        if obj.author != self.request.user:
            raise PermissionDenied('You do not have permission to edit.')
 
        return super(UpdateView, self).dispatch(request, *args, **kwargs)

class DeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = Article
    success_url = reverse_lazy('gpt:index')


class IndexView(generic.ListView):
    model = Article

class DetailView(generic.DetailView):
    model = Article