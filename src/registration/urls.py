from django.urls import path, include
from django.contrib.auth.views import LogoutView
from registration.views import CustomLoginView, CustomSignUpView, CustomPasswordChangeView, CustomPasswordResetView
from . import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', CustomSignUpView.as_view(), name='signup'),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]
