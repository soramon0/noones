from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('signin/', views.signin),
    path('update-password/', views.update_password)
]
