from django.urls import path

from . import views

urlpatterns = [
    path('', views.models, name='models'),
    path('<uuid:id>', views.model, name='model'),
    path('request', views.contact, name='request'),
    path('subset', views.subset, name='subset'),
    path('search', views.search, name='search'),
]