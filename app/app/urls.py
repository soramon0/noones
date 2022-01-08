from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns

urlpatterns = i18n_patterns(
    # Website URLS
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('models/', include('models.urls')),
    path('accounts/', include('accounts.urls')),
)

urlpatterns += [
    # API endpoints
    path('api/v1/', include('core.api.urls')),
    path('api/v1/models/', include('models.api.urls')),
    path('api/v1/accounts/', include('accounts.api.urls')),
    path('api/v1/update/', include('updates.api.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
