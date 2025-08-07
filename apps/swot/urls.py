from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.swot.views import (
    CompanySWOTOptionViewSet,
    SWOTOptionViewSet,
    SWOTQuestionViewSet,
)
from apps.swot.views.swot import (
    CompanySWOTOptionAnalysisViewSet,
    CompanySWOTOptionMatrixViweSet,
    CompanySWOTQuestionAnalysisViewSet,
    CompanySWOTQuestionMatrixViweSet,
    CompanySWOTQuestionViewSet,
)

router = DefaultRouter()

router.register("options", SWOTOptionViewSet, basename="options")
router.register("questions", SWOTQuestionViewSet, basename="questions")


company_swot_router = DefaultRouter()
company_swot_router.register(
    "questions/matrix/analysis",
    CompanySWOTQuestionAnalysisViewSet,
    basename="question-matrix-analysis",
)
company_swot_router.register(
    "options/matrix/analysis",
    CompanySWOTOptionAnalysisViewSet,
    basename="option-matrix-analysis",
)
company_swot_router.register(
    "questions/matrix", CompanySWOTQuestionMatrixViweSet, basename="question-matrix"
)
company_swot_router.register(
    "options/matrix", CompanySWOTOptionMatrixViweSet, basename="option-matrix"
)
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
