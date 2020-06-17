from django.urls import path

from updates.api import views

app_name = 'updates'

urlpatterns = [
    path('measures/', views.create_measures_update),
    path('measures/<uuid:measure_id>/', views.MeasuresUpdateAPIView.as_view()),
    path('gallery/', views.get_or_create_gallery),
    path('gallery/<int:update_id>/', views.GalleryUpdateAPIView.as_view()),
    path('gallery/related_photo/<int:id>/', views.updateGallery)
]
