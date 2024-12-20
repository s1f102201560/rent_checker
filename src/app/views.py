import random
import string
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_safe, require_http_methods
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from app.models import ChatLog, ChatRoom, Consultation
from app.forms import ContactForm, ConsultationForm, FileForm

def generate_url(request):
    room_name = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    base_url = request.build_absolute_uri().rstrip('/')
    if base_url.endswith('/new'):
        base_url = base_url[:-4]
    full_url = f"{base_url}/chat-{room_name}"
    return full_url

def top(request):
    return render(request, "app/top.html")

@login_required
@require_safe
def consultation(request):
    consultations = Consultation.objects.all()
    context = {
        "consultations": consultations,
    }
    return render(request, 'app/consultation.html', context)

@login_required
def consultation_detail(request, consultation_id):
    consultation = get_object_or_404(Consultation, pk=consultation_id)
    context = {
        "consultation": consultation,
    }
    return render(request, "app/consultation_detail.html", context)

@login_required
@require_http_methods(["GET", "POST", "HEAD"])
def consultation_new(request):
    if request.method == "POST":
        form = ConsultationForm(request.POST)
        if form.is_valid():
            consultation = form.save(commit=False)
            consultation.user = request.user
            consultation.room_link = generate_url(request)
            chat_room = ChatRoom.objects.create(name=consultation.title, link=consultation.room_link, user=request.user)
            consultation.room = chat_room
            if request.FILES:
                consultation.file = request.FILES.get('file')
            consultation.save()
            return redirect(consultation_detail, consultation_id=consultation.pk)
    else:
        form = ConsultationForm()
        context = {
            "form": form,
        }
        return render(request, "app/consultation_new.html", context)

@login_required
def consultation_edit(request, consultation_id):
    consultation = get_object_or_404(Consultation, pk=consultation_id)
    if consultation.user.id != request.user.id:
        return HttpResponseForbidden("この相談の編集は許可されていません")
    if request.method == "POST":
        form = ConsultationForm(request.POST, instance=consultation)
        if form.is_valid():
            if request.FILES:
                consultation.file = request.FILES.get('file')
            form.save()
            return redirect("consultation_detail", consultation_id=consultation_id)
    else:
        form = ConsultationForm(instance=consultation)
        context = {
            "form": form,
        }
        return render(request, "app/consultation_edit.html", context)


@login_required
def chat(request, room_url):
    full_url = request.build_absolute_uri().rstrip('/')
    consultation = Consultation.objects.get(room_link=full_url)
    room, created = ChatRoom.objects.get_or_create(
        link=full_url,
        defaults={"name": consultation.title}
    )
    chat_logs = ChatLog.objects.filter(room=room, user=request.user).order_by('created_at')
    room_logs = ChatRoom.objects.filter().distinct().order_by('-created_at')

    return render(request, 'app/chat.html', {
        'room_name': room_url,
        'chat_logs': chat_logs,
        'room_logs': room_logs,
    })

# 画像アップロード処理
@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()  # 画像を保存
            image_url = image.file.url  # 画像のURLを取得
            return JsonResponse({'status': 'success', 'image_url': image_url})
        else:
            return JsonResponse({'status': 'error', 'message': form.errors.as_json()})
    else:
        form = FileForm()
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