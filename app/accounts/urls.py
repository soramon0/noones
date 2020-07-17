from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from . import forms

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('profile/', views.profile, name='profile'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset_form.html',
        html_email_template_name='accounts/password_reset_email.html',
        form_class=forms.ResetPasswordForm
    ),
        name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html',
    ),
        name='password_reset_done'
    ),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html',
        form_class=forms.SetNewPasswordForm
    ),
        name='password_reset_confirm'
    ),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts//password_reset_complete.html'
    ),
        name='password_reset_complete'
    ),
    path('activate/<uidb64>/<token>',
         views.ActivateAccount.as_view(), name='activate'),
]
