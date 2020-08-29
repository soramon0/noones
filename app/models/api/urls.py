from django.urls import path

from . import views

app_name = 'models'

urlpatterns = [
    path('me/', views.me, name='me'),
    path('', views.ListModels.as_view(), name='list_models'),
    path('<uuid:pk>/', views.UpdateModel.as_view(), name='update_model'),
    path('search/', views.SearchModels.as_view(), name='search_models'),
    path('contact/', views.contact_model, name='contact_model'),
    path('photos/profile/',
         views.ListPorfilePictures.as_view(), name='list_profile_pictures'),
    path('photos/profile/<uuid:picture_id>/',
         views.ProfilePictureAPIView.as_view(), name='delete_profile_picture'),
    path('photos/profile/<uuid:picture_id>/mark/',
         views.mark_as_profile_picture, name='mark_profile_picture'),
    path('photos/cover/',
         views.ListCoverPictures.as_view(), name='list_cover_pictures'),
    path('photos/cover/<uuid:picture_id>/',
         views.CoverPictureAPIView.as_view(), name='delete_cover_picture'),
    path('photos/cover/<uuid:picture_id>/mark/',
         views.mark_as_cover_picture, name='mark_cover_picture')
]
