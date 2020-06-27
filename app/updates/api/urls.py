from django.urls import path

from updates.api import views

app_name = 'updates'

urlpatterns = [
    path('measures/', views.create_measures_update),
    path('measures/<uuid:measure_id>/', views.MeasuresUpdateAPIView.as_view()),
    path('photos/gallery/', views.get_or_create_gallery),
    path('photos/gallery/<int:update_id>/',
         views.GalleryUpdateAPIView.as_view()),
    path('photos/gallery/related_photo/<int:id>/', views.updateGallery),
    path('photos/profile/', views.get_or_create_profile_photo_update),
    path('photos/profile/<int:update_id>/',
         views.ProfilePictureUpdateAPIView.as_view())
]
