from rest_framework.serializers import ModelSerializer

from apps.swot.models import (
    SWOTModelMatrix,
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


class SWOTMatrixSerialiezr(ModelSerializer):
    class Meta:
        model = SWOTModelMatrix
        fields = [
            "id",
            "matrix_type",
            "opportunity",
            "threat",
            "weakness",
            "strength",
            "created_at",
        ]


class SWOTTypeMatrixSerializer(ModelSerializer):
    class Meta:
        model = SWOTModelMatrix
        fields = [
            "id",
            "opportunity",
            "threat",
            "weakness",
            "strength",
            "created_at",
            "updated_at",
            "deleted_at",
        ]

    def create(self, validated_data):
        validated_data["company"] = self.context["company"]
        return super().create(validated_data)
