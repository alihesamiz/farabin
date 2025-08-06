from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from apps.swot.repositories import SWOTRepository as _repo
from apps.swot.serializers import (
    CompanySWOTOptionAnalysisSerializer,
    CompanySWOTOptionManageSerializer,
    CompanySWOTOptionMatrixManageSerializer,
    CompanySWOTOptionMatrixSerializer,
    CompanySWOTOptionSerializer,
    CompanySWOTQuestionAnalysisSerializer,
    CompanySWOTQuestionManageSerializer,
    CompanySWOTQuestionMatrixManageSerializer,
    CompanySWOTQuestionMatrixSerializer,
    CompanySWOTQuestionSerializer,
    SWOTOptionSerializer,
    SWOTQuestionSerializer,
)
from apps.swot.views import ViewSetMixin


class SWOTOptionViewSet(ViewSetMixin, ModelViewSet):
    http_method_names = ["get"]
    default_serializer_class = SWOTOptionSerializer
    queryset = _repo.get_swot_options()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category"]


class SWOTQuestionViewSet(ViewSetMixin, ModelViewSet):
    http_method_names = ["get"]
    queryset = _repo.get_swot_questions()
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
        query_param = self.request.query_params.get("category")
        company = self.get_company()
        return _repo.get_swot_options_of_company(company, query_param)


class CompanySWOTQuestionViewSet(ViewSetMixin, ModelViewSet):
    action_serializer_class = {
        "list": CompanySWOTQuestionSerializer,
        "retrieve": CompanySWOTQuestionSerializer,
        "create": CompanySWOTQuestionManageSerializer,
        "update": CompanySWOTQuestionManageSerializer,
        "partial_update": CompanySWOTQuestionManageSerializer,
    }

    def get_queryset(self):
        query_param = self.request.query_params.get("category")
        company = self.get_company()
        return _repo.get_swot_questions_of_company(company, query_param)


class CompanySWOTQuestionMatrixViweSet(ViewSetMixin, ModelViewSet):
    action_serializer_class = {
        "list": CompanySWOTQuestionMatrixSerializer,
        "retrieve": CompanySWOTQuestionMatrixSerializer,
        "create": CompanySWOTQuestionMatrixManageSerializer,
        "update": CompanySWOTQuestionMatrixManageSerializer,
        "partial_update": CompanySWOTQuestionMatrixManageSerializer,
    }

    def get_queryset(self):
        query_param = self.request.query_params.get("category")
        company = self.get_company()
        return _repo.get_swot_questions_matrix_of_company(company, query_param)


class CompanySWOTOptionMatrixViweSet(ViewSetMixin, ModelViewSet):
    action_serializer_class = {
        "list": CompanySWOTOptionMatrixSerializer,
        "retrieve": CompanySWOTOptionMatrixSerializer,
        "create": CompanySWOTOptionMatrixManageSerializer,
        "update": CompanySWOTOptionMatrixManageSerializer,
        "partial_update": CompanySWOTOptionMatrixManageSerializer,
    }

    def get_queryset(self):
        query_param = self.request.query_params.get("category")
        company = self.get_company()
        return _repo.get_swot_options_matrix_of_company(company, query_param)


class CompanySWOTQuestionAnalysisViewSet(ViewSetMixin, ModelViewSet):
    http_method_names = ["get"]
    default_serializer_class = CompanySWOTQuestionAnalysisSerializer

    def get_queryset(self):
        company = self.get_company()
        return _repo.get_swot_question_analysis_of_company(company)


class CompanySWOTOptionAnalysisViewSet(ViewSetMixin, ModelViewSet):
    http_method_names = ["get"]
    default_serializer_class = CompanySWOTOptionAnalysisSerializer

    def get_queryset(self):
        company = self.get_company()
        return _repo.get_swot_option_analysis_of_company(company)
