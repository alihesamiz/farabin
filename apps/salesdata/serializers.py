from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils.timezone import now
from rest_framework.serializers import ModelSerializer, SlugRelatedField

from apps.salesdata.models import (
    CustomerSaleData,
    CustomerSaleFile,
    ProductData,
    ProductDataFile,
)
from constants.errors.errors import (
    CustomerAlreadyExistsError,
    ProductAlreadyExistsError,
)


class ProductBaseSerializer(ModelSerializer):
    class Meta:
        model = ProductData
        fields = [
            "id",
            "name",
            "code",
            "updated_at",
        ]


class ProductListSerializer(ProductBaseSerializer): ...


class ProductSerializer(ModelSerializer):
    class Meta(ProductBaseSerializer.Meta):
        fields = ProductBaseSerializer.Meta.fields + [
            "unit",
            "description",
            "created_at",
            "deleted_at",
        ]


class ProductCreateSerializer(ModelSerializer):
    class Meta:
        model = ProductData
        fields = [
            "name",
            "code",
            "unit",
            "description",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["company"] = getattr(user.company_user, "company", None)

        try:
            return super().create(validated_data)
        except IntegrityError:
            raise ProductAlreadyExistsError


class ProductUpdateSerializer(ModelSerializer):
    class Meta:
        model = ProductData
        fields = [
            "name",
            "code",
            "unit",
            "description",
        ]

    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except IntegrityError:
            raise ProductAlreadyExistsError


class CompanyCustomerListSerializer(ModelSerializer):
    city = SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = CustomerSaleData
        fields = [
            "id",
            "sale_area",
            "name",
            "city",
            "last_purchase_date",
            "updated_at",
        ]


class CompanyCustomerSerializer(ModelSerializer):
    city = SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = CustomerSaleData
        fields = [
            "id",
            "name",
            "sale_area",
            "channel",
            "city",
            "area",
            "description",
            "first_purchase_date",
            "last_purchase_date",
            "created_at",
            "updated_at",
            "deleted_at",
        ]


class CompanyCustomerCreateSerializer(ModelSerializer):
    class Meta:
        model = CustomerSaleData
        fields = [
            "name",
            "sale_area",
            "channel",
            "city",
            "area",
            "first_purchase_date",
            "last_purchase_date",
            "description",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["company"] = getattr(user.company_user, "company", None)

        try:
            return super().create(validated_data)
        except IntegrityError:
            raise CustomerAlreadyExistsError


class CompanyCustomerUpdateSerializer(ModelSerializer):
    class Meta:
        model = CustomerSaleData
        fields = [
            "name",
            "sale_area",
            "channel",
            "city",
            "area",
            "first_purchase_date",
            "last_purchase_date",
            "description",
        ]

    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except IntegrityError:
            raise CustomerAlreadyExistsError


class CompanyCustomerFileSerializer(ModelSerializer):
    class Meta:
        model = CustomerSaleFile
        fields = [
            "id",
            "file",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        read_only_fields = [
            "deleted_at",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        company = getattr(user.company_user, "company", None)
        if not company:
            raise ValidationError("User has no associated company")

        validated_data["company"] = company
        return CustomerSaleFile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if validated_data["deleted_at"]:
            instance.deleted_at = now()

        instance.save()
        return instance


class CompanyProductFileSerializer(ModelSerializer):
    class Meta:
        model = ProductDataFile
        fields = [
            "id",
            "file",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        read_only_fields = [
            "deleted_at",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        company = getattr(user.company_user, "company", None)
        if not company:
            raise ValidationError("User has no associated company")

        validated_data["company"] = company
        return ProductDataFile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if validated_data["deleted_at"]:
            instance.deleted_at = now()

        instance.save()
        return instance
