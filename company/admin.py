from typing import Any


from django.utils.translation import gettext_lazy as _
from django.db.models.query import QuerySet
from django.db.transaction import atomic
from django.http import HttpRequest
from django.contrib import messages
from django.db import transaction
from django.contrib import admin


from company.models import CompanyProfile, CompanyService, LifeCycle



class LifeCycleInline(admin.StackedInline):
    model = LifeCycle
    extra = 0
    min_num = 1
    max_num = 1

@admin.register(LifeCycle)
class LifeCycleAdmin(admin.ModelAdmin):
    list_display = ['capital_providing',]


@admin.register(CompanyProfile)
class CompanyAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']
    search_fields = ['company_title', 'manager_name']
    list_display = ['company_title', 'national_code', 'manager_name',
                    'tech_field', 'special_field_display', 'license', 'insurance_list', 'capital_providing_method_display']

    readonly_fields = ['id']

    filter_horizontal = ('capital_providing_method',)

    @admin.display(ordering='national_code')
    def national_code(self, company_profile: CompanyProfile):
        return company_profile.user.national_code
    national_code.short_description = _("National Code")

    def special_field_display(self, company_profile: CompanyProfile):
        return company_profile.special_field  # Ensure this matches the field name
    special_field_display.short_description = _("Special Field")

    @admin.display(description=_("Capital Providing Method"), ordering='capital_providing_method_display')
    def capital_providing_method_display(self, company_profile: CompanyProfile):
        return ", ".join([cycle.get_capital_providing_display() for cycle in company_profile.capital_providing_method.all()])


@admin.register(CompanyService)
class CompanyServiceAdmin(admin.ModelAdmin):
    autocomplete_fields = ['company']
    list_display = ['company', 'service', 'is_active', 'purchased_date']

    search_fields = ['company__company_title',
                     'service__description', 'purchased_date']

    @admin.action(description=_("Activate selected services"))
    def activate_services(self, request, queryset):
        updated_count = queryset.update(is_active=True)
        self.message_user(
            request,
            _("{} service(s) were successfully marked as active.").format(
                updated_count),
            messages.SUCCESS
        )

    @admin.action(description=_("Deactivate selected services"))
    def deactivate_services(self, request, queryset):
        updated_count = queryset.update(is_active=False)
        self.message_user(
            request,
            _("{} service(s) were successfully marked as deactive.").format(
                updated_count),
            messages.SUCCESS
        )

    # Add the action to the actions list
    actions = [activate_services, deactivate_services]
