from django.urls import path

from . import views

urlpatterns = [
    path('models/me/', views.me, name='me'),
    path('models/<uuid:pk>/', views.ModelAPIView.as_view()),
    path('measures/<uuid:pk>/', views.MeasuresAPIView.as_view()),
]
