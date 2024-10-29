from django.db import IntegrityError
from rest_framework.exceptions import ValidationError

from rest_framework import serializers

from django.contrib.auth import get_user_model

from django.utils.translation import gettext_lazy as _

from .models import BalanceReport, CompanyProfile, CompanyService, TaxDeclaration

User = get_user_model()


# class DashboardSerializer(serializers.ModelSerializer):
#     company_title = serializers.CharField(
#         source='company_service.company.company_title', read_only=True)
#     service_name = serializers.CharField(
#         source='company_service.service.name', read_only=True)
#     is_active = serializers.BooleanField(
#         source='company_service.is_active', read_only=True)
#     purchased_date = serializers.DateTimeField(
#         source='company_service.purchased_date', read_only=True)

#     class Meta:
#         model = Dashboard
#         fields = ['id', 'company_title', 'service_name',
#                   'is_active', 'purchased_date']


class CompanyServiceSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.name', read_only=True)

    class Meta:
        model = CompanyService
        fields = ['id', 'service_name', 'is_active', 'purchased_date']


class CompanyProfileSerializer(serializers.ModelSerializer):
    user_national_code = serializers.CharField(
        source='user.national_code', read_only=True)
    services = CompanyServiceSerializer(
        many=True, read_only=True)  # Remove `source='services'`

    class Meta:
        model = CompanyProfile
        fields = [

            'user_national_code', 'id',
            'company_title',  'social_code', 'email', 'manager_name',
            'license', 'special_field', 'tech_field',  'province', 'city',
            'insurance_list', 'capital_providing_method',
            'profile_active', 'services', 'address'
        ]
        # read_only_fields = ['user_national_code']

    def update(self, instance, validated_data):
        # Handle the many-to-many field separately
        capital_providing_methods = validated_data.pop(
            'capital_providing_method', [])

        # Update the fields of the instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Save the instance
        instance.save()

        # Update the many-to-many field after saving the instance
        if capital_providing_methods:
            instance.capital_providing_method.set(capital_providing_methods)

        return instance


class CompanyProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = [
            'id',
            'company_title',  'social_code', 'email', 'manager_name',
            'license', 'special_field', 'tech_field',  'province', 'city',
            'insurance_list', 'capital_providing_method',
            'profile_active', 'address'
        ]

    def validate_email(self, value):
        # Check if the email is already used by another company profile
        request = self.context.get('request')
        # Get current profile ID if it exists
        profile_id = self.instance.id if self.instance else None

        if CompanyProfile.objects.filter(email=value).exclude(id=profile_id).exists():
            raise ValidationError(
                "This email is already associated with another company profile.")
        return value

    def validate_social_code(self, value):
        request = self.context.get('request')
        profile_id = self.instance.id if self.instance else None

        if CompanyProfile.objects.filter(social_code=value).exclude(id=profile_id).exists():
            raise ValidationError(
                "This Social Code is already associated with another company profile.")
        return value

    def create(self, validated_data):
        capital_providing_methods = validated_data.pop(
            'capital_providing_method', [])
        user = self.context['request'].user

        try:
            # Create the CompanyProfile object with the user
            company_profile, created = CompanyProfile.objects.get_or_create(
                user=user, defaults=validated_data)

            # If the profile already existed, update it
            if not created:
                for attr, value in validated_data.items():
                    setattr(company_profile, attr, value)
                company_profile.save()

            # Update the many-to-many field after saving the instance
            company_profile.capital_providing_method.set(
                capital_providing_methods)
            return company_profile

        except IntegrityError:
            raise ValidationError(
                {"email": "A company profile with this email or social code already exists."})

    def update(self, instance, validated_data):
        capital_providing_methods = validated_data.pop(
            'capital_providing_method', [])

        # Run the validate_email method if email is part of the update data
        if 'email' in validated_data:
            self.validate_email(validated_data['email'])

        # Update the fields of the instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        try:
            # Save the instance
            instance.save()

            # Update the many-to-many field after saving the instance
            instance.capital_providing_method.set(capital_providing_methods)
            return instance

        except IntegrityError:
            raise ValidationError(
                {"email": "A company profile with this email already exists."})


class BalanceReportCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceReport
        fields = ['year', 'balance_report_file',
                  'profit_loss_file', 'sold_product_file','account_turnover_file']

    def create(self, validated_data):
        # Get the current user
        user = self.context['request'].user

        # Get the user's company
        company = CompanyProfile.objects.get(user=user)

        # Assign the company to the BalanceReport
        validated_data['company'] = company

        # Check if a report for the same company and year exists
        year = validated_data.get('year')
        existing_report = BalanceReport.objects.filter(
            company=company, year=year).first()

        if existing_report:
            # If a report exists, return it (skip creating a new one)
            return existing_report

        # Create a new report if it doesn't exist
        return super().create(validated_data)


class BalanceReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceReport
        fields = ['id', 'year', 'balance_report_file',
                  'profit_loss_file', 'sold_product_file','account_turnover_file']


class TaxDeclarationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxDeclaration
        fields = ['year', 'tax_file']

    def create(self, validated_data):
        # Get the current user
        user = self.context['request'].user

        # Get the user's company
        company = CompanyProfile.objects.get(user=user)

        # Assign the company to the TaxDeclaration
        validated_data['company'] = company

        # Create the TaxDeclaration
        return super().create(validated_data)


class TaxDeclarationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxDeclaration
        fields = ['id',  'year', 'tax_file']
