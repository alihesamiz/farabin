from rest_framework.routers import DefaultRouter

from apps.swot.views import (
    SWOTMatrixViweSet,
    SWOTOptionViewSet,
    SWOTQuestionViewSet,
)

router = DefaultRouter()

router.register("options", SWOTOptionViewSet, basename="options")
router.register("questions", SWOTQuestionViewSet, basename="questions")
router.register("matrix", SWOTMatrixViweSet, basename="matrix")

urlpatterns = router.urls
