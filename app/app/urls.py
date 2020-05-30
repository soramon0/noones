from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # Website URLS 
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('models/', include('models.urls')),
    path('accounts/', include('accounts.urls')),

    # API endpoints
    path('api/v1/models/', include('models.api.urls')),
    path('api/v1/accounts/', include('accounts.api.urls')),
    path('api/v1/clones/', include('clones.api.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
