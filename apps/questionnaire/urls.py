from rest_framework.routers import DefaultRouter

from apps.questionnaire.views.questionnair import CompanyQuestionnaireViewSet

router = DefaultRouter()

router.register(r"", CompanyQuestionnaireViewSet, basename="questionnaire")


urlpatterns = router.urls
