from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from app.views import top, sandbox, sandbox_room, upload_image

index_view = TemplateView.as_view(template_name="app/index.html")

urlpatterns = [
    path('', top, name="top"),
    path('index/', login_required(index_view), name="index"),
    path('sandbox/', login_required(sandbox), name="sandbox"),
    path("sandbox/<str:room_name>/", login_required(sandbox_room), name="room"),
    path('upload_image/', upload_image, name='upload_image'),
]
