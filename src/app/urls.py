from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from app.views import top, chat, upload_image, ContactFormView, ContactResultView

index_view = TemplateView.as_view(template_name="app/index.html")

urlpatterns = [
    path('', top, name="top"),
    path('index/', login_required(index_view), name="index"),
    path("chat/<str:room_name>/", login_required(chat), name="chat"),
    path('upload_image/', upload_image, name='upload_image'),
    path('contact/', ContactFormView.as_view(), name='contact_form'), # 問い合わせフォーム
    path('contact/result/', ContactResultView.as_view(), name='contact_result'), #問い合わせフォーム結果
]
