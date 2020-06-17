from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('vision-et-mission/', views.vision, name='vision'),
    path('a-propos/', views.apropos, name='a-propos'),
]
