from rest_framework.serializers import ModelSerializer

from apps.swot.models import (
    SWOTAnalysis,
    SWOTMatrix,
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
        model = SWOTMatrix
        fields = [
            "id",
            "matrix_type",
            "opportunity",
            "threat",
            "weakness",
            "strength",
            "created_at",
        ]


class SWOTMatrixTypeSerializer(ModelSerializer):
    class Meta:
        model = SWOTMatrix
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


class SWOTAnalysisListSerializer(ModelSerializer):
    class Meta:
        model = SWOTAnalysis
        fields = [
            "id",
            "so",
            "st",
            "wo",
            "wt",
            "created_at",
        ]


class SWOTAnalysisSerializer(ModelSerializer):
    class Meta:
        model = SWOTAnalysis
        fields = [
            "so",
            "st",
            "wo",
            "wt",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
