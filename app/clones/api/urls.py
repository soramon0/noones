from django.urls import path

from clones.api import views

app_name = 'clones'

urlpatterns = [
    path('measures/', views.create_measures_clone),
    path('measures/<uuid:pk>/', views.MeasuresCloneAPIView.as_view()),
    path('gallery/', views.create_photo_clone)
]
