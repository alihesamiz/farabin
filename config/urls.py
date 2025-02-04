from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "مدیریت وبسایت فرابین"

urlpatterns = [
    path('farabin-admin/', admin.site.urls),

    path('diagnostic/', include('diagnostics.urls')),

    path('management/', include('management.urls')),
    
    path('company/', include('company.urls')),

    path('tickets/', include('ticket.urls')),

    path('auth/', include('core.urls')),

    path('management/', include('management.urls')),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += [
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

        path('api/schema/swagger-ui/',
             SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

        path('api/schema/redoc/',
             SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]

urlpatterns += [
    re_path(r'^i18n/', include('django.conf.urls.i18n')),
]
