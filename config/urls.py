from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("farabin-admin/", admin.site.urls),
    path("management/", include("apps.management.urls")),
    path("packages/", include("apps.packages.urls")),
    path("finance/", include("apps.finance.urls")),
    path("company/", include("apps.company.urls")),
    path("sales/", include("apps.salesdata.urls")),
    path("tickets/", include("apps.tickets.urls")),
    path("auth/", include("apps.core.urls")),
    path("swot/", include("apps.swot.urls")),
    path("questionnaire/", include("apps.questionnaire.urls")),
    path("balancesheet/", include("apps.balancesheet.urls")),

]


if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += [
        path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
        path(
            "swagger/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger",
        ),
        path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    ] + debug_toolbar_urls()

urlpatterns += [
    re_path(r"^i18n/", include("django.conf.urls.i18n")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
