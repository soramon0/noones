from django.urls import path

from . import views

urlpatterns = [
    path('', views.list_models, name='models'),
    path('<uuid:id>', views.detail_model, name='model'),
    path('search', views.search_models, name='search'),
]
