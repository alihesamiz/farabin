from dateutil.relativedelta import relativedelta
from datetime import datetime
from core.models import Service
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


# class CompanyServiceSerializer(serializers.ModelSerializer):
#     service_name = serializers.CharField(source='service.name', read_only=True)


#     class Meta:
#         model = CompanyService
#         fields = ['id', 'service_name', 'is_active', 'purchased_date']


# class CompanyServiceSerializer(serializers.ModelSerializer):
#     all_services = serializers.SerializerMethodField()

#     class Meta:
#         model = CompanyService
#         fields = ['all_services']

#     def get_all_services(self, obj):
#         # Get all services
#         all_services = Service.objects.all()

#         # Retrieve company-specific services for the related company
#         company_services = CompanyService.objects.filter(company=obj.company)

#         # Map active services by service ID to their activation details
#         active_services = {cs.service_id: cs for cs in company_services}

#         # Build a list of all services with their active status and purchase date
#         services_data = []
#         for service in all_services:
#             service_data = {
#                 'service_name': service.name,
#                 'description': service.description,
#                 'price': service.price,
#                 'is_active': service.id in active_services,
#                 'purchased_date': active_services[service.id].purchased_date if service.id in active_services else None
#             }
#             services_data.append(service_data)

#         return services_data


# class CompanyProfileSerializer(serializers.ModelSerializer):
#     user_national_code = serializers.CharField(
#         source='user.national_code', read_only=True)
#     services = CompanyServiceSerializer(
#         many=True, read_only=True)  # Remove `source='services'`

#     class Meta:
#         model = CompanyProfile
#         fields = [

#             'user_national_code', 'id',
#             'company_title',  'social_code', 'email', 'manager_name',
#             'license', 'special_field', 'tech_field',  'province', 'city',
#             'insurance_list', 'capital_providing_method',
#             'profile_active', 'services', 'address'
#         ]
#         # read_only_fields = ['user_national_code']

#     def update(self, instance, validated_data):
#         # Handle the many-to-many field separately
#         capital_providing_methods = validated_data.pop(
#             'capital_providing_method', [])

#         # Update the fields of the instance
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)

#         # Save the instance
#         instance.save()

#         # Update the many-to-many field after saving the instance
#         if capital_providing_methods:
#             instance.capital_providing_method.set(capital_providing_methods)

#         return instance
class CompanyServiceSerializer(serializers.Serializer):
    # Directly define the fields for each service entry
    service_name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=20, decimal_places=0)
    is_active = serializers.BooleanField()
    purchased_date = serializers.DateField(allow_null=True)


class CompanyProfileSerializer(serializers.ModelSerializer):
    user_national_code = serializers.CharField(
        source='user.national_code', read_only=True
    )
    # Single call to fetch all services
    services = serializers.SerializerMethodField()

    class Meta:
        model = CompanyProfile
        fields = [
            'user_national_code', 'id', 'company_title', 'social_code', 'email',
            'manager_name', 'license', 'special_field', 'tech_field', 'province',
            'city', 'insurance_list', 'capital_providing_method', 'profile_active',
            'address', 'services',
        ]

    def get_services(self, obj):
        # Retrieve all services available
        all_services = Service.objects.all()

        # Get active services for this company
        company_services = CompanyService.objects.filter(company=obj)
        active_services = {cs.service_id: cs for cs in company_services}

        # Format the response data for each service
        services_data = [
            {
                'service_name': service.name,
                'description': service.description,
                # 'price': service.price,
                'is_active': service.id in active_services,
                'purchased_date': active_services[service.id].purchased_date
                if service.id in active_services else None,
                "expiration_date":  active_services[service.id].purchased_date + relativedelta(months=3)
                if service.id in active_services else None
            }
            for service in all_services
        ]

        return services_data


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
        fields = ['year', 'month', 'balance_report_file',
                  'profit_loss_file', 'sold_product_file', 'account_turnover_file', 'is_saved', 'is_sent']

    def create(self, validated_data):
        # Get the current user
        user = self.context['request'].user

        # Get the user's company
        company = CompanyProfile.objects.get(user=user)

        # Assign the company to the BalanceReport
        validated_data['company'] = company

        # Check if a report for the same company and year exists
        year = validated_data.get('year')
        month = validated_data.get('month')
        existing_report = BalanceReport.objects.filter(
            company=company, year=year, month=month).first()

        if existing_report:
            raise ValidationError(
                {"error": "This months' file already exists"})

        # Create a new report if it doesn't exist
        return super().create(validated_data)


class BalanceReportSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()

    class Meta:
        model = BalanceReport
        fields = ['id', 'year', 'month', 'balance_report_file',
                  'profit_loss_file', 'sold_product_file', 'account_turnover_file', 'is_saved', 'is_sent']


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

        year = validated_data.get('year')
        existing_report = TaxDeclaration.objects.filter(
            company=company, year=year).first()

        if existing_report:
            raise ValidationError(
                {"error": "This years' file already exists"})

        # Create the TaxDeclaration
        return super().create(validated_data)


class TaxDeclarationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxDeclaration
        fields = ['id',  'year', 'tax_file', 'is_saved', 'is_sent']
