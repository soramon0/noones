from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
 	path('signin', views.signin, name="api_signin"), 
]