from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView
from .forms import CustomLoginForm, CustomSignUpForm, CustomPasswordChangeForm, CustomPasswordResetForm

class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_type'] = 'login'
        return context

class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_type'] = 'password_change'
        return context

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_type'] = 'password_reset'
        return context

class CustomSignUpView(CreateView):
    form_class = CustomSignUpForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_type'] = 'signup'
        return context

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .models import CustomUser

def register(request):
    if request.method == 'POST':
        # フォームの処理とユーザ作成
        user = CustomUser.objects.create_user(...)
        user.is_active = False  # メール確認前は非アクティブ
        user.save()

        # メール送信
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        mail_subject = 'Activate your account.'
        message = render_to_string('registration/acc_active_email.html', {
            'user': user,
            'domain': request.get_host(),
            'uid': uid,
            'token': token,
        })
        send_mail(mail_subject, message, 'from@example.com', [user.email])

        return redirect('registration_complete')
    else:
        # フォームの表示
        pass

from django.contrib.auth import login
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import get_object_or_404

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'registration/activation_invalid.html')
