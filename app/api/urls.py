from django.urls import path

from .views import ModelAPIView

urlpatterns = [
    path('models/me/', ModelAPIView.as_view(), name='me'),
]
