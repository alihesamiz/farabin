from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [

    path('farabin-admin/', admin.site.urls),

    path('management/', include('management.urls')),

    path('finance/', include('finance.urls')),

    path('company/', include('company.urls')),

    path('requests/', include('request.urls')),

    path('tickets/', include('tickets.urls')),

    path('auth/', include('core.urls')),

]
if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += [
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

        path('swagger/',
             SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),

        path('redoc/',
             SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ] + debug_toolbar_urls()

urlpatterns += [
    re_path(r'^i18n/', include('django.conf.urls.i18n')),
]
urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)
