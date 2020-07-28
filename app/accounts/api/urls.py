from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('signin/', views.signin),
    path('update_password/', views.update_password),
    path('update_email/', views.update_email)
]
