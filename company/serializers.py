from rest_framework.exceptions import ValidationError

from rest_framework import serializers

from django.contrib.auth import get_user_model

from django.utils.translation import gettext_lazy as _

from .models import BalanceReport, CompanyProfile, CompanyService, Dashboard, TaxDeclaration

User = get_user_model()


class DashboardSerializer(serializers.ModelSerializer):
    company_title = serializers.CharField(
        source='company_service.company.company_title', read_only=True)
    service_name = serializers.CharField(
        source='company_service.service.name', read_only=True)
    is_active = serializers.BooleanField(
        source='company_service.is_active', read_only=True)
    purchased_date = serializers.DateTimeField(
        source='company_service.purchased_date', read_only=True)

    class Meta:
        model = Dashboard
        fields = ['id', 'company_title', 'service_name',
                  'is_active', 'purchased_date']


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

    def create(self, validated_data):
        capital_providing_methods = validated_data.pop(
            'capital_providing_method', [])

        # Pass the user (which should be provided by the view)
        user = self.context['request'].user

        # Create the CompanyProfile object with the user
        company_profile, created = CompanyProfile.objects.get_or_create(
            user=user, defaults=validated_data)

        # If the profile already existed (created is False), update it
        if not created:
            for attr, value in validated_data.items():
                setattr(company_profile, attr, value)
            company_profile.save()

        # Update the many-to-many field after saving the instance
        company_profile.capital_providing_method.set(capital_providing_methods)

        return company_profile


# class TaxDeclarationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TaxDeclaration
#         fields = ['id', 'company', 'year', 'tax_file']
        
#     def create(self, validated_data):
#         # Get the current user
#         user = self.context['request'].user
        
#         # Get the user's company
#         company = CompanyProfile.objects.get(user=user)
        
#         # Assign the company to the TaxDeclaration
#         validated_data['company'] = company
        
#         # Create the TaxDeclaration
#         return super().create(validated_data)


# class BalanceReportSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BalanceReport
#         fields = ['id', 'company', 'company_id', 'year', 'balance_report_file',
#                   'prift_loss_file', 'sold_product_file']
        
#     # def create(self, validated_data):
#     #     company = validated_data.get('company')
#     #     year = validated_data.get('year')

#     #     # Check if a record for the same company and year exists
#     #     existing_report = BalanceReport.objects.filter(company=company, year=year).first()

#     #     if existing_report:
#     #         # Skip file upload or handle as needed
#     #         return existing_report

#     #     # Create a new report if it doesn't exist
#     #     return super().create(validated_data)
#     def create(self, validated_data):
#         # Get the current user
#         user = self.context['request'].user
        
#         # Get the user's company
#         company = CompanyProfile.objects.get(user=user)

#         # Assign the company to the BalanceReport
#         validated_data['company'] = company

#         # Check if a report for the same company and year exists
#         year = validated_data.get('year')
#         existing_report = BalanceReport.objects.filter(company=company, year=year).first()

#         if existing_report:
#             # If a report exists, return it (skip creating a new one)
#             return existing_report

#         # Create a new report if it doesn't exist
#         return super().create(validated_data)


class BalanceReportCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceReport
        fields = [ 'year', 'balance_report_file',
                  'prift_loss_file', 'sold_product_file']

    def create(self, validated_data):
        # Get the current user
        user = self.context['request'].user
        
        # Get the user's company
        company = CompanyProfile.objects.get(user=user)

        # Assign the company to the BalanceReport
        validated_data['company'] = company

        # Check if a report for the same company and year exists
        year = validated_data.get('year')
        existing_report = BalanceReport.objects.filter(company=company, year=year).first()

        if existing_report:
            # If a report exists, return it (skip creating a new one)
            return existing_report

        # Create a new report if it doesn't exist
        return super().create(validated_data)


class BalanceReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceReport
        fields = ['id', 'company', 'year', 'balance_report_file',
                  'prift_loss_file', 'sold_product_file']



class TaxDeclarationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxDeclaration
        fields = [ 'year', 'tax_file']
        
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
        fields = ['id', 'company', 'year', 'tax_file']
