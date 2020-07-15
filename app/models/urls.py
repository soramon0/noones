from django.urls import path

from . import views

urlpatterns = [
    path('', views.list_models, name='models'),
    path('<uuid:id>', views.detail_model, name='model'),
    path('request', views.model_contact, name='request'),
    path('search', views.model_search, name='search'),
]
