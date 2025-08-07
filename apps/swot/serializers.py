from rest_framework.serializers import ModelSerializer

from apps.swot.models import (
    CompanySWOTOption,
    CompanySWOTOptionAnalysis,
    CompanySWOTOptionMatrix,
    CompanySWOTQuestion,
    CompanySWOTQuestionAnalysis,
    CompanySWOTQuestionMatrix,
    SWOTOption,
    SWOTQuestion,
)


class SWOTOptionSerializer(ModelSerializer):
    class Meta:
        model = SWOTOption
        fields = [
            "id",
            "option",
            "category",
        ]


class SWOTQuestionSerializer(ModelSerializer):
    class Meta:
        model = SWOTQuestion
        fields = [
            "id",
            "text",
            "category",
        ]


class CompanySWOTOptionSerializer(ModelSerializer):
    options = SWOTOptionSerializer(many=True, read_only=True)

    class Meta:
        model = CompanySWOTOption
        fields = ["id", "options"]


class CompanySWOTOptionManageSerializer(ModelSerializer):
    class Meta:
        model = CompanySWOTOption
        fields = ["id", "options"]
        read_only_fields = ["id"]

    def create(self, validated_data: dict):
        options = validated_data.pop("options", [])
        company = self.context["company"]

        instance, created = CompanySWOTOption.objects.get_or_create(
            company=company,
        )

        if not created:
            instance.options.add(*options)
        else:
            instance.options.set(options)

        return instance

    def update(self, instance: CompanySWOTOption, validated_data: dict):
        options = validated_data.pop("options", None)

        if options is not None:
            instance.options.set(options)

        return super().update(instance, validated_data)


class CompanySWOTQuestionSerializer(ModelSerializer):
    question = SWOTQuestionSerializer(read_only=True)

    class Meta:
        model = CompanySWOTQuestion
        fields = ["id", "question", "answer", "category", "external_factor"]


class CompanySWOTQuestionManageSerializer(ModelSerializer):
    class Meta:
        model = CompanySWOTQuestion
        fields = ["id", "question", "answer", "category", "external_factor"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        validated_data["company"] = self.context["company"]
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class CompanySWOTOptionMatrixSerializer(ModelSerializer):
    options = CompanySWOTOptionSerializer(many=True, read_only=True)

    class Meta:
        model = CompanySWOTOptionMatrix
        fields = [
            "id",
            "options",
            "created_at",
            "updated_at",
            "deleted_at",
        ]


class CompanySWOTOptionMatrixManageSerializer(ModelSerializer):
    class Meta:
        model = CompanySWOTOptionMatrix
        fields = ["options"]

    def create(self, validated_data):
        options = validated_data.pop("options")
        company = self.context["company"]
        validated_data["company"] = company
        matrix, created = CompanySWOTOptionMatrix.objects.get_or_create(
            company=company, defaults=validated_data
        )
        if not created:
            matrix.options.add(options)
        else:
            matrix.options.set(options)
        return matrix

    def update(self, instance: CompanySWOTOptionMatrix, validated_data: dict):
        options = validated_data.pop("options", None)
        if options is not None:
            instance.options.set(options)
        return super().update(instance, validated_data)


class CompanySWOTQuestionMatrixSerializer(ModelSerializer):
    questions = CompanySWOTQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = CompanySWOTQuestionMatrix
        fields = [
            "id",
            "questions",
            "created_at",
            "updated_at",
            "deleted_at",
        ]


class CompanySWOTQuestionMatrixManageSerializer(ModelSerializer):
    class Meta:
        model = CompanySWOTQuestionMatrix
        fields = ["questions"]

    def create(self, validated_data):
        questions = validated_data.pop("questions")
        company = self.context["company"]
        validated_data["company"] = company
        matrix, created = CompanySWOTQuestionMatrix.objects.get_or_create(
            company=company, defaults=validated_data
        )
        if not created:
            matrix.questions.add(questions)
        else:
            matrix.questions.set(questions)
        return matrix

    def update(self, instance: CompanySWOTQuestionMatrix, validated_data: dict):
        questions = validated_data.pop("questions", None)
        if questions is not None:
            instance.questions.set(questions)
        return super().update(instance, validated_data)


class CompanySWOTQuestionAnalysisSerializer(ModelSerializer):
    class Meta:
        model = CompanySWOTQuestionAnalysis
        fields = [
            "id",
            "matrix",
            "so",
            "st",
            "wo",
            "wt",
            "created_at",
            "updated_at",
            "deleted_at",
        ]


class CompanySWOTOptionAnalysisSerializer(ModelSerializer):
    class Meta:
        model = CompanySWOTOptionAnalysis
        fields = [
            "id",
            "matrix",
            "so",
            "st",
            "wo",
            "wt",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
