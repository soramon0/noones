from django.urls import path

from updates.api import views

app_name = 'updates'

urlpatterns = [
    path('measures/', views.create_measures_update),
    path('measures/<uuid:pk>/', views.MeasuresUpdateAPIView.as_view()),
    path('gallery/', views.create_gallery),
]
