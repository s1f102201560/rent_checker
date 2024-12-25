from django.urls import path
from django.contrib.auth.decorators import login_required
from app.views import top, chat, consultation, search_consultations,  consultation_detail, consultation_new, consultation_edit, consultation_delete, consultation_bulk_delete, upload_image, ContactFormView, ContactResultView, template, security_deposit, before_move, brokerage_fee, penalty_fee, restoration, insurance


urlpatterns = [
    path('', top, name="top"),
    path('consultation/', consultation, name="consultation"),
    path('search-consultation/', search_consultations, name="search_consultations"),
    path("consultation/new/", consultation_new, name="consultation_new"),
    path("consultation/<int:consultation_id>/", consultation_detail, name="consultation_detail"),
    path("consultation/<int:consultation_id>/edit/", consultation_edit, name="consultation_edit"),
    path("consultation/<int:consultation_id>/delete/", consultation_delete, name="consultation_delete"),
    path("consultation/bulk-delete/", consultation_bulk_delete, name="consultation_bulk_delete"),
    path("consultation/<str:room_url>/", login_required(chat), name="chat"),
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
