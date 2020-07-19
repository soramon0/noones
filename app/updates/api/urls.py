from django.urls import path
from rest_framework.routers import DefaultRouter

from updates.api import views

app_name = 'updates'

router = DefaultRouter()

router.register(r'model', views.ModelUpdateViewSet, basename='model-update')
router.register(r'measures', views.MeasuresUpdateViewSet,
                basename='measures-update')

urlpatterns = [
    path('photos/gallery/', views.get_or_create_gallery_update),
    path('photos/gallery/<int:update_id>/',
         views.GalleryUpdateAPIView.as_view()),
    path('photos/gallery/related_photo/<int:id>/', views.update_gallery),
    path('photos/profile/', views.get_or_create_profile_picture_update),
    path('photos/profile/<int:update_id>/',
         views.ProfilePictureUpdateAPIView.as_view()),
    path('photos/cover/', views.get_or_create_cover_picture_update),
    path('photos/cover/<int:update_id>/',
         views.CoverPictureUpdateAPIView.as_view()),
] + router.urls
