from django.urls import path

from . import views

app_name = 'models'

urlpatterns = [
    path('me/', views.me, name='me'),
    path('<uuid:pk>/', views.ModelAPIView.as_view()),
    path('measures/<uuid:pk>/', views.MeasuresAPIView.as_view()),
    path('photos/profile/', views.ProfilePictureAPIView.as_view()),
    path('photos/cover/', views.CoverPictureAPIView.as_view()),
    path('photos/gallery/', views.gallery),
    path('photos/gallery/<int:pk>', views.GalleryAPIView.as_view()),
]
