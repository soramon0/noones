from django.urls import path

from updates.api import views

app_name = 'updates'

urlpatterns = [
    path('measures/', views.create_measures_update),
    path('measures/<uuid:measure_id>/', views.MeasuresUpdateAPIView.as_view()),
    path('photos/gallery/', views.get_or_create_gallery_update),
    path('photos/gallery/<int:update_id>/',
         views.GalleryUpdateAPIView.as_view()),
    path('photos/gallery/related_photo/<int:id>/', views.updateGallery),
    path('photos/profile/', views.get_or_create_profile_picture_update),
    path('photos/profile/<int:update_id>/',
         views.ProfilePictureUpdateAPIView.as_view()),
    path('photos/cover/', views.get_or_create_cover_picture_update),
    path('photos/cover/<int:update_id>/',
         views.CoverPictureUpdateAPIView.as_view()),
]
