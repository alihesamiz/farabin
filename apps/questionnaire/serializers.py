from rest_framework.serializers import (
    IntegerField,
    ModelSerializer,
    PrimaryKeyRelatedField,
    Serializer,
    SerializerMethodField,
)
from rest_framework import serializers

from apps.questionnaire.models import (
    CompanyAnswer,
    CompanyQuestionnaire,
    Question,
    QuestionChoice,
    QuestionMetric,
    Questionnaire,
)


class QuestionMetricSerializer(ModelSerializer):
    class Meta:
        model = QuestionMetric
        fields = ["id", "title", "weight"]


class QuestionChoiceSerializer(ModelSerializer):
    class Meta:
        model = QuestionChoice
        fields = ["id", "answer", "points"]


class CompanyAnswerSerializer(ModelSerializer):
    selected_choice = QuestionChoiceSerializer(read_only=True)
    selected_choice_id = PrimaryKeyRelatedField(
        queryset=QuestionChoice.objects.all(), source="selected_choice", write_only=True
    )
    question_id = PrimaryKeyRelatedField(
        queryset=Question.objects.all(), source="question", write_only=True
    )

    class Meta:
        model = CompanyAnswer
        fields = [
            "id",
            "selected_choice",
            "selected_choice_id",
            "question_id",
            "answered_at",
        ]
        read_only_fields = ["id", "answered_at"]

    def create(self, validated_data):
        validated_data["company"] = self.context["company"]
        return super().create(validated_data)


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "text", "order"]

    def to_representation(self, instance):
        """
        If the question is being serialized through the QuestionnaireQuestion model,
        add the 'order' field to the representation.
        """
        representation = super().to_representation(instance)
        if hasattr(instance, "order"):
            representation["order"] = instance.order
        return representation

    def create(self, validated_data):
        validated_data["company"] = self.context["company"]
        return super().create(validated_data)


class QuestionRetrieveSerializer(ModelSerializer):
    choices = QuestionChoiceSerializer(many=True, read_only=True)
    metrics = QuestionMetricSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = [
            "id",
            "text",
            "choices",
            "metrics",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        validated_data["company"] = self.context["company"]
        return super().create(validated_data)


class QuestionWithAnswerSerializer(QuestionRetrieveSerializer):
    company_answer = SerializerMethodField()

    class Meta(QuestionRetrieveSerializer.Meta):
        fields = QuestionRetrieveSerializer.Meta.fields + ["company_answer"]

    def get_company_answer(self, obj):
        company_questionnaire = self.context.get("company_questionnaire")
        if not company_questionnaire:
            return None

        try:
            answer = company_questionnaire.answers.get(question=obj)
            return CompanyAnswerSerializer(answer).data
        except CompanyAnswer.DoesNotExist:
            return None

    def create(self, validated_data):
        validated_data["company"] = self.context["company"]
        return super().create(validated_data)


class QuestionnaireSerializer(ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = ["id", "name", "created_at", "counter"]

    def create(self, validated_data):
        validated_data["company"] = self.context["company"]
        return super().create(validated_data)


class QuestionnaireWithAnswersSerializer(ModelSerializer):
    questions = QuestionWithAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Questionnaire
        fields = ["id", "name", "counter", "questions", "created_at", "updated_at"]

    def create(self, validated_data):
        validated_data["company"] = self.context["company"]
        return super().create(validated_data)


class CompanyQuestionnaireSerializer(ModelSerializer):
    questionnaire = QuestionnaireSerializer(read_only=True)
    questionnaire_id = PrimaryKeyRelatedField(
        queryset=Questionnaire.objects.all(), source="questionnaire", write_only=True
    )

    class Meta:
        model = CompanyQuestionnaire
        #fields = ["id", "questionnaire", "questionnaire_id",  "question_counter", "submitted_at"]
        fields = ["id", "questionnaire", "questionnaire_id",  "submitted_at"]
        read_only_fields = [
            "id",
            "submitted_at",
        ]

    def create(self, validated_data):
        validated_data["company"] = self.context["company"]
        return super().create(validated_data)



class CompanyQuestionnaireRetrieveSerializer(serializers.ModelSerializer):
    questionnaire = QuestionnaireWithAnswersSerializer(read_only=True)
    questionnaire_id = serializers.CharField(source="questionnaire.id", read_only=True)  

    class Meta:
        model = CompanyQuestionnaire
        fields = ["id", "questionnaire", "questionnaire_id", "submitted_at"]

    def to_representation(self, instance):
        self.context["company_questionnaire"] = instance
        return super().to_representation(instance)

    def create(self, validated_data):
        if "company" not in self.context:
            raise serializers.ValidationError("Company context is required.")
        validated_data["company"] = self.context["company"]
        return super().create(validated_data)
    


 
# class CompanyQuestionnaireRetrieveSerializer(ModelSerializer):
#     questionnaire = QuestionnaireWithAnswersSerializer(read_only=True)

#     # it is using CompanyQuestionnaire model but this model doesnt have id field -> get the wuestion aire id from companyquestionaire and retreive it
#     class Meta:
#         model = CompanyQuestionnaire
#         fields = ["id", "questionnaire", "submitted_at"]

#     def to_representation(self, instance):
#         self.context["company_questionnaire"] = instance
#         return super().to_representation(instance)

#     def create(self, validated_data):
#         validated_data["company"] = self.context["company"]
#         return super().create(validated_data)



class AnswerSubmissionSerializer(Serializer):
    """
    A simple serializer to validate the payload for submitting answers.
    It does not interact with the database, just validates the input format.
    """

    question_id = IntegerField(required=True)
    selected_choice_id = IntegerField(required=True)

    class Meta:
        fields = ["question_id", "selected_choice_id"]

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
