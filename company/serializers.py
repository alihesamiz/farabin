from dateutil.relativedelta import relativedelta
from datetime import datetime
from core.models import Service
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import BalanceReport, BaseRequest, CompanyProfile, CompanyService, DiagnosticRequest, TaxDeclaration
User = get_user_model()


class CompanyServiceSerializer(serializers.Serializer):
    service_name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=20, decimal_places=0)
    is_active = serializers.BooleanField()
    purchased_date = serializers.DateField(allow_null=True)


class CompanyProfileSerializer(serializers.ModelSerializer):
    user_national_code = serializers.CharField(
        source='user.national_code', read_only=True
    )
    services = serializers.SerializerMethodField()

    class Meta:
        model = CompanyProfile
        fields = [
            'user_national_code', 'id', 'company_title', 'social_code', 'email',
            'manager_name', 'license', 'special_field', 'tech_field', 'province',
            'city', 'insurance_list', 'capital_providing_method', 'profile_active',
            'address', 'services',
        ]

    def get_services(self, company)-> list[str]:
        # Retrieve all services available
        all_services = Service.objects.filter(service_active=True)

        # Get active services for this company
        company_services = CompanyService.objects.filter(company=company)
        active_services = {
            cs.service_id: cs for cs in company_services if cs.is_active
        }
        # Format the response data for each service
        services_data = [
            {
                'id': service.id,
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

# TODO : if user service time is expired the service will be removed


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
        user = self.context['request'].user
        company = CompanyProfile.objects.get(user=user)
        validated_data['company'] = company

        year = validated_data.get('year')
        month = validated_data.get('month')
        existing_report = BalanceReport.objects.filter(company=company, year=year, month=month).first()

        if existing_report:
            raise ValidationError({"error": "This months' file already exists"})
        
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Handle file updates
        for field in ['balance_report_file', 'profit_loss_file', 'sold_product_file', 'account_turnover_file']:
            new_file = validated_data.get(field)
            if new_file and getattr(instance, field) != new_file:
                # Delete old file before saving the new one
                old_file = getattr(instance, field)
                if old_file:
                    old_file.delete()  # Delete the old file

        return super().update(instance, validated_data)


class BalanceReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceReport
        fields = ['id', 'year', 'month', 'balance_report_file',
                  'profit_loss_file', 'sold_product_file', 'account_turnover_file', 'is_saved', 'is_sent']


class SimpleBalanceReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceReport
        fields = ['id', 'year', 'month',]


class TaxDeclarationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxDeclaration
        fields = ['year', 'tax_file']

    def create(self, validated_data):
        user = self.context['request'].user
        company = CompanyProfile.objects.get(user=user)
        validated_data['company'] = company

        year = validated_data.get('year')
        existing_report = TaxDeclaration.objects.filter(company=company, year=year).first()

        if existing_report:
            raise ValidationError({"error": "This years' file already exists"})
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Handle file update
        tax_file = validated_data.get('tax_file', None)
        if tax_file and instance.tax_file != tax_file:
            # Optionally, you can handle file replacement here too
            old_file = instance.tax_file
            if old_file:
                old_file.delete()  # Delete the old file before saving the new one

        return super().update(instance, validated_data)


class TaxDeclarationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxDeclaration
        fields = ['id',  'year', 'tax_file', 'is_saved', 'is_sent']


class SimpleTaxDeclarationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxDeclaration
        fields = ['id',  'year']


class BaseRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseRequest
        fields = ['id', 'status', 'subject', 'created_at', 'updated_at']

    def update(self, instance, validated_data):
        # Custom update logic if needed
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class DiagnosticRequestSerializer(BaseRequestSerializer):
    tax_record = SimpleTaxDeclarationSerializer()
    balance_record = SimpleBalanceReportSerializer()

    class Meta(BaseRequestSerializer.Meta):
        model = DiagnosticRequest
        fields = BaseRequestSerializer.Meta.fields + \
            ['tax_record', 'balance_record']
