from rest_framework.serializers import ModelSerializer

from apps.swot.models import (
    CompanySWOTOption,
    CompanySWOTQuestion,
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
