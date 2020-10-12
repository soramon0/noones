from django.urls import path

from core.api import views

app_name = "core"

urlpatterns = [
    path("country/", views.list_countries),
    path("city/", views.list_cities)
]
