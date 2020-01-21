from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('models/', include('models.urls')),
    path('accounts/', include('accounts.urls')),
]
