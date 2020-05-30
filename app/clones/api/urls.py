from django.urls import path

from clones.api import views

app_name = 'clones'

urlpatterns = [
    path('measures/', views.create_measures_clone),
    path('measures/<uuid:measures_id>/<uuid:clone_id>', views.MeasuresCloneAPIView.as_view()),
]