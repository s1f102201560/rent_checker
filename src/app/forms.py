from django import forms
from app.models import Image
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.conf import settings
from django import forms

class ImageForm(forms.ModelForm):
    MAX_FILE_SIZE_MB = 20  # 最大ファイルサイズ (MB)

    class Meta:
        model = Image
        fields = ['file']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            max_file_size = self.MAX_FILE_SIZE_MB * 1024 * 1024  # MB をバイトに変換
            if file.size > max_file_size:
                raise forms.ValidationError(
                    f'ファイルサイズは {self.MAX_FILE_SIZE_MB}MB 以下にしてください。'
                )
        return file

# 問い合わせフォーム
class ContactForm(forms.Form):
    name = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "お名前",
        }),
    )
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': "メールアドレス",
        }),
    )
    message = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': "お問い合わせ内容",
        }),
    )

    def send_email(self, user):
        subject = "お問い合わせ"
        if user.is_authenticated:
            username = user.username
        else:
            username = "Anonymous"
        
        # 送信者へのメッセージ内容
        user_message = "以下の内容でお問い合わせを受け付けました。\n\nお名前: {name} 様\nメールアドレス: {email}\nお問い合わせ内容:\n{message}\n\nこのメールは自動返信メールとなっておりますのでこのメールアドレスに直接連絡いただいても返信できません。ご了承ください。なお、返信は1~2日程を目安に返信いたします。".format(
            name=self.cleaned_data['name'],
            email=self.cleaned_data['email'],
            message=self.cleaned_data['message']
        )

        # 管理者へのメッセージ内容
        admin_message = "送信者名: {name} 様\nメールアドレス: {email}\nお問い合わせ内容:\n{message}\n\nログインユーザー: {username}\n".format(
            name=self.cleaned_data['name'],
            email=self.cleaned_data['email'],
            message=self.cleaned_data['message'],
            username=username
        )
        
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [settings.EMAIL_HOST_USER]
        
        try:
            # 管理者へのメール送信
            send_mail(subject, admin_message, from_email, recipient_list)
            
            # 送信者へのメール送信
            send_mail("お問い合わせありがとうございます", user_message, from_email, [self.cleaned_data['email']])
        except BadHeaderError:
            return HttpResponse("無効なヘッダが検出されました。")
