from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from apps.swot.models import (
    CompanySWOTOption,
    CompanySWOTQuestion,
    SWOTOption,
    SWOTQuestion,
)
from apps.swot.serializers import (
    CompanySWOTOptionManageSerializer,
    CompanySWOTOptionSerializer,
    CompanySWOTQuestionManageSerializer,
    CompanySWOTQuestionSerializer,
    SWOTOptionSerializer,
    SWOTQuestionSerializer,
)
from apps.swot.views.mixin import ViewSetMixin


class SWOTOptionViewSet(ViewSetMixin, ModelViewSet):
    http_method_names = ["get"]
    default_serializer_class = SWOTOptionSerializer
    queryset = SWOTOption.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category"]


class SWOTQuestionViewSet(ViewSetMixin, ModelViewSet):
    http_method_names = ["get"]
    queryset = SWOTQuestion.objects.all()
    default_serializer_class = SWOTQuestionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category"]


class CompanySWOTOptionViewSet(ViewSetMixin, ModelViewSet):
    action_serializer_class = {
        "list": CompanySWOTOptionSerializer,
        "retrieve": CompanySWOTOptionSerializer,
        "create": CompanySWOTOptionManageSerializer,
        "update": CompanySWOTOptionManageSerializer,
        "partial_update": CompanySWOTOptionManageSerializer,
    }

    def get_queryset(self):
        company = self.get_company()
        return (
            CompanySWOTOption.objects.select_related("company")
            .prefetch_related("options")
            .filter(company=company)
        )


class CompanySWOTQuestionViewSet(ViewSetMixin, ModelViewSet):
    action_serializer_class = {
        "list": CompanySWOTQuestionSerializer,
        "retrieve": CompanySWOTQuestionSerializer,
        "create": CompanySWOTQuestionManageSerializer,
        "update": CompanySWOTQuestionManageSerializer,
        "partial_update": CompanySWOTQuestionManageSerializer,
    }

    def get_queryset(self):
        company = self.get_company()
        return CompanySWOTQuestion.objects.select_related("company", "question").filter(
            company=company
        )
