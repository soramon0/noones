from django.urls import path

from . import views

app_name = 'models'

urlpatterns = [
    path('me/', views.me),
    path('', views.ListModels.as_view()),
    path('<uuid:pk>/', views.UpdateModel.as_view()),
    path('search/', views.SearchModels.as_view()),
    path('contact/', views.model_contact),
    path('photos/profile/', views.ListPorfilePictures.as_view()),
    path('photos/profile/<int:picture_id>/',
         views.ProfilePictureAPIView.as_view()),
    path('photos/profile/<int:picture_id>/mark/', views.mark_as_profile_picture),
    path('photos/cover/', views.ListCoverPictures.as_view()),
    path('photos/cover/<int:picture_id>/', views.CoverPictureAPIView.as_view()),
    path('photos/cover/<int:picture_id>/mark/', views.mark_as_cover_picture)
]
