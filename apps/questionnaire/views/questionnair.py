from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.questionnaire.repository.questionnaire_repo import (
    QuestionnaireRepository as _repo,
)
from apps.questionnaire.serializers import (
    AnswerSubmissionSerializer,
    CompanyAnswerSerializer,
    CompanyQuestionnaireRetrieveSerializer,
    CompanyQuestionnaireSerializer,
)
from apps.questionnaire.views.mixin import ViewSetMixin
from django.utils import timezone

# class CompanyQuestionnaireViewSet(ViewSetMixin, ModelViewSet):
#     action_serializer_class = {"retrieve": CompanyQuestionnaireRetrieveSerializer}
#     default_serializer_class = CompanyQuestionnaireSerializer


#     def get_queryset(self):
#         return _repo.get_company_questionnaire(company=self.get_company())


class CompanyQuestionnaireViewSet(ViewSetMixin, ModelViewSet):
    # Use the more specific serializer for the retrieve action
    action_serializer_class = {
        "retrieve": CompanyQuestionnaireRetrieveSerializer,
        "submit_answers": AnswerSubmissionSerializer,
    }
    default_serializer_class = CompanyQuestionnaireSerializer

    def get_queryset(self):
        company = self.get_company()
        return _repo.get_company_questionnaires(company=company)

    def get_object(self):
        obj = _repo.get_company_questionnaire_detail(pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj



    @action(detail=True, methods=["post"], url_path="submit-answers")
    def submit_answers(self, request, pk=None):
        """
        Custom action to submit a batch of answers for a questionnaire.
        Expects a list of answer objects in the request body.
        Example Body:
        [
            {"question_id": 1, "selected_choice_id": 3},
            {"question_id": 2, "selected_choice_id": 5}
        ]
        """
        company_questionnaire = self.get_object()
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        
        try:
            _repo.bulk_create_or_update_answers(
                company_questionnaire=company_questionnaire,
                answers_data=serializer.validated_data,
            )
            # Update the submitted_at field with the current timestamp
            company_questionnaire.submitted_at = timezone.now()
            company_questionnaire.save()
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(
            {"status": "Answers submitted successfully"},
            status=status.HTTP_200_OK
        )