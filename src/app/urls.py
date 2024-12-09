from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from app.views import top, chat, document, document_detail, document_new, document_edit, upload_image, ContactFormView, ContactResultView, template, security_deposit, before_move, brokerage_fee, penalty_fee, restoration, insurance

index_view = TemplateView.as_view(template_name="app/index.html")

urlpatterns = [
    path('', top, name="top"),
    path('index/', login_required(index_view), name="index"),
    path('document/', document, name="document"),
    path("document/new/", document_new, name="document_new"),
    path("<int:document_id>/", document_detail, name="document_detail"),
    path("<int:document_id>/edit/", document_edit, name="document_edit"),
    path("chat/<str:room_name>/", login_required(chat), name="chat"),
    path('upload_image/', upload_image, name='upload_image'),
    path('contact/', ContactFormView.as_view(), name='contact_form'), # 問い合わせフォーム
    path('contact/result/', ContactResultView.as_view(), name='contact_result'), #問い合わせフォーム結果
    path('template', template, name='template'), # 本番では削除する
    path('security_deposit', security_deposit, name='security_deposit'),
    path('before_move', before_move, name='before_move'),
    path('brokerage_fee', brokerage_fee, name='brokerage_fee'),
    path('penalty_fee', penalty_fee, name='penalty_fee'),
    path('restoration', restoration, name='restoration'),
    path('insurance', insurance, name='insurance'),
]
