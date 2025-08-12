from rest_framework.routers import DefaultRouter

from apps.swot.views import (
    SWOTMatrixViweSet,
    SWOTOptionViewSet,
    SWOTQuestionViewSet,
)
from apps.swot.views.swot import SWOTAnalysisViewSet

router = DefaultRouter()

router.register("options", SWOTOptionViewSet, basename="options")
router.register("questions", SWOTQuestionViewSet, basename="questions")
router.register("matrix", SWOTMatrixViweSet, basename="matrix")
router.register("analysis", SWOTAnalysisViewSet, basename="analysis")

urlpatterns = router.urls
