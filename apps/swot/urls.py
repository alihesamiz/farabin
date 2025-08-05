from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.swot.views import (
    CompanySWOTOptionViewSet,
    SWOTOptionViewSet,
    SWOTQuestionViewSet,
)
from apps.swot.views.swot import CompanySWOTQuestionViewSet

router = DefaultRouter()

router.register("options", SWOTOptionViewSet, basename="options")
router.register("questions", SWOTQuestionViewSet, basename="questions")


company_swot_router = DefaultRouter("company")
company_swot_router.register(
    "options", CompanySWOTOptionViewSet, basename="company-swot-options"
)
company_swot_router.register(
    "questions", CompanySWOTQuestionViewSet, basename="company-swot-questions"
)

urlpatterns = [
    path("company/", include(company_swot_router.urls)),
]

urlpatterns += router.urls
