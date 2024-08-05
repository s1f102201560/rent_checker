from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from gpt import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('registration/', include('registration.urls')),
    path('gpt/', include('gpt.urls')),
    re_path(r'^media/uploads/(?P<path>.*)$', views.protected_media, name='protected_media'),
]