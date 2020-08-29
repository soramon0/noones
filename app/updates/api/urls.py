from django.urls import path
from rest_framework.routers import DefaultRouter

from updates.api import views

app_name = "updates"

router = DefaultRouter()

router.register(r"profile", views.ProfileUpdateViewSet, basename="profile-updates")
router.register(r"measures", views.MeasuresUpdateViewSet, basename="measures-updates")
router.register(
    r"photos/gallery", views.GalleryUpdateViewSet, basename="gallery-updates"
)
router.register(
    r"photos/profile",
    views.ProfilePictureUpdateViewSet,
    basename="profile-picture-updates",
)
router.register(
    r"photos/cover",
    views.CoverPictureUpdateViewSet,
    basename="cover-picture-updates",
)

urlpatterns = [
    path(
        "photos/gallery/related_photo/<uuid:related_photo_id>/",
        views.ChangeOrCreateGalleryUpdate.as_view(),
    ),
    # path("photos/cover/", views.get_or_create_cover_picture_update),
    # path("photos/cover/<uuid:update_id>/", views.CoverPictureUpdateAPIView.as_view()),
] + router.urls
