from django.urls import path

from . import views

urlpatterns = [
    path('models/me/', views.me, name='me'),
]
