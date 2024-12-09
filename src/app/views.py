from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_safe, require_http_methods
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from app.models import ChatLog, ChatRoom, Document
from app.forms import ContactForm, DocumentForm, ImageForm

def top(request):
    return render(request, "app/top.html")

def index(request):
    return render(request, 'app/index.html')

@require_safe
def document(request):
    documents = Document.objects.all()
    context = {
        "documents": documents,
    }
    return render(request, 'app/document.html', context)

def document_detail(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    context = {
        "document": document,
    }
    return render(request, "app/document_detail.html", context)

@login_required
@require_http_methods(["GET", "POST", "HEAD"])
def document_new(request):
    if request.method == "POST":
        form = DocumentForm(request.POST)
        if form.is_valid():
            document = form.save(commit=False)
            document.author = request.user
            document.save()
            return redirect(document_detail, document_id=document.pk)
    else:
        form = DocumentForm()
        context = {
            "form": form,
        }
        return render(request, "app/document_new.html", context)

@login_required
def document_edit(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    if document.author.id != request.user.id:
        return HttpResponseForbidden("この相談の編集は許可されていません")
    if request.method == "POST":
        form = DocumentForm(request.POST, instance=document)
        if form.is_valid():
            form.save()
            return redirect("document_detail", document_id=document_id)
    else:
        form = DocumentForm(instance=document)
        context = {
            "form": form,
        }
        return render(request, "app/document_edit.html", context)


def chat(request, room_name):
    room, created = ChatRoom.objects.get_or_create(name=room_name)
    chat_logs = ChatLog.objects.filter(room=room, user=request.user).order_by('created_at')
    room_logs = ChatRoom.objects.filter(chat_logs__user=request.user).distinct().order_by('-created_at')
    return render(request, 'app/chat.html', {
        'room_name': room_name,
        'chat_logs': chat_logs,
        'room_logs': room_logs,
    })

# 画像アップロード処理
@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()  # 画像を保存
            image_url = image.file.url  # 画像のURLを取得
            return JsonResponse({'status': 'success', 'image_url': image_url})
        else:
            return JsonResponse({'status': 'error', 'message': form.errors.as_json()})
    else:
        form = ImageForm()
    return render(request, 'app/chat.html', {'form': form})


#問い合わせフォーム
class ContactFormView(FormView):
    template_name = 'app/info/contact_form.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact_result')

    def form_valid(self, form):
        form.send_email(self.request.user)
        return super().form_valid(form)



class ContactResultView(TemplateView):
    template_name = 'app/info/contact_result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['success'] = "お問い合わせは正常に送信されました。ご入力いただいたメールアドレスに入力内容を自動返信しております。返信があるまでしばらくお待ちください。なお、自動返信メールが届かない場合や返信がない場合はメールアドレスが間違っている可能性がありますので、その際はお手数ですがもう一度ご入力お願いいたします。"
        return context


# これはテンプレートの確認用 本番では消す
def template(request):
    return render(request, "app/info/template.html")

def security_deposit(request):
    return render(request, "app/info/security_deposit.html")

def before_move(request):
    return render(request, "app/info/before_move.html")

def brokerage_fee(request):
    return render(request, "app/info/brokerage_fee.html")

def restoration(request):
    return render(request, "app/info/restoration.html")

def penalty_fee(request):
    return render(request, "app/info/penalty_fee.html")

def insurance(request):
    return render(request, "app/info/insurance.html")