from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from apps.swot.repositories import SWOTRepository as _repo
from apps.swot.serializers import (
    SWOTAnalysisListSerializer,
    SWOTAnalysisSerializer,
    SWOTMatrixRetrieveSerialiezr,
    SWOTMatrixSerialiezr,
    SWOTMatrixTypeSerializer,
    SWOTOptionSerializer,
    SWOTQuestionSerializer,
)
from apps.swot.views import BasePagination, ViewSetMixin
from constants.responses import APIResponse


class SWOTOptionViewSet(ViewSetMixin, ModelViewSet):
    action_serializer_class = {}
    http_method_names = ["get"]
    default_serializer_class = SWOTOptionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category"]

    def get_queryset(self):
        return _repo.get_swot_options()


class SWOTQuestionViewSet(ViewSetMixin, ModelViewSet):
    action_serializer_class = {}
    http_method_names = ["get"]
    default_serializer_class = SWOTQuestionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category"]

    def get_queryset(self):

        return _repo.get_swot_questions()


class SWOTMatrixViweSet(ViewSetMixin, ModelViewSet):
    action_serializer_class = {
        "retrieve": SWOTMatrixRetrieveSerialiezr,
        "questionnaire_matrix": SWOTMatrixTypeSerializer,
        "inferential_matrix": SWOTMatrixTypeSerializer,
        "elective_matrix": SWOTMatrixTypeSerializer,
    }
    default_serializer_class = SWOTMatrixSerialiezr
    pagination_class = BasePagination

    def get_queryset(self):
        company = self.get_company()
        return _repo.get_swot_matrix_of_company(company)

    def handle_matrix_action(self, request, matrix_type, serializer_class):
        if request.method.lower() == "get":
            qs = self.get_queryset().filter(matrix_type=matrix_type)
            serializer = serializer_class(
                qs, many=True, context=self.get_serializer_context()
            )
            return APIResponse.success(data=serializer.data)

        elif request.method.lower() == "post":
            data = request.data.copy()
            data["matrix_type"] = matrix_type
            serializer = serializer_class(
                data=data, context=self.get_serializer_context()
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(company=self.get_company())
            return APIResponse.success(data=serializer.data)

    @action(
        methods=["get", "post"], detail=False, url_path="q-matrix", url_name="q_matrix"
    )
    def questionnaire_matrix(self, request):
        return self.handle_matrix_action(request, "q", SWOTMatrixTypeSerializer)

    @action(
        methods=["get", "post"], detail=False, url_path="i-matrix", url_name="i_matrix"
    )
    def inferential_matrix(self, request):
        return self.handle_matrix_action(request, "i", SWOTMatrixTypeSerializer)

    @action(
        methods=["get", "post"], detail=False, url_path="e-matrix", url_name="e_matrix"
    )
    def elective_matrix(self, request):
        return self.handle_matrix_action(request, "e", SWOTMatrixTypeSerializer)


class SWOTAnalysisViewSet(ViewSetMixin, ReadOnlyModelViewSet):
    action_serializer_class = {
        "list": SWOTAnalysisListSerializer,
        "retrieve": SWOTAnalysisSerializer,
    }

    def get_queryset(self):
        return _repo.get_swot_analysis_of_company(self.get_company())
