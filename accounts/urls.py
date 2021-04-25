from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    HomePageView,
    RegisterView,
    LogInView,
    LogOutView,
    ResetPasswordView,
)

urlpatterns = [
    path('', HomePageView, name='home'),
    path('register/', RegisterView, name='register'),
    path('login/', LogInView, name='login'),
    path('logout/', LogOutView, name='logout'),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         ResetPasswordView.as_view(
             template_name='accounts/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]