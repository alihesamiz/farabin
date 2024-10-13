from .models import CompanyService, Service, Dashboard
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import City, CompanyProfile, Institute, Organization, Province, User, AccountTurnOver, FinancialAsset, LifeCycle, ProfitLossStatement, SoldProductFee, BalanceReport, TaxDeclarationFile

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'national_code',
                    'is_active', 'is_staff', 'is_superuser')

    # Define the fields to search for in the search bar
    search_fields = ('phone_number', 'national_code')

    # Define the ordering of the users
    ordering = ('phone_number',)

    # Define which fields to show on the 'add' or 'change' pages
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        (_('Personal info'), {'fields': ('national_code',)}),
        (_('Permissions'), {
         'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )

    # Define the fields to display when creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'national_code', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

    # Fields that are read-only in the admin interface
    readonly_fields = ('last_login',)

    # Remove filter_horizontal since 'groups' and 'user_permissions' do not exist
    filter_horizontal = ()

    # Remove 'groups' from list_filter
    list_filter = ('is_active', 'is_staff', 'is_superuser')


@admin.register(CompanyProfile)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['company_title', 'national_code',
                    'manager_name', 'tech_field', 'insurance_list']

    readonly_fields = ['id']

    @admin.display(ordering='national_code')
    def national_code(self, company_profile: CompanyProfile):
        return company_profile.user.national_code
    national_code.short_description = _("National Code")


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass


@admin.register(Institute)
class InstituteAdmin(admin.ModelAdmin):
    list_display = ['title', 'province']
    autocomplete_fields = ['province']
    search_fields = ['title']

# Admin for Province


class CityAdminInline(admin.StackedInline):
    model = City
    extra = 0
    min_num = 0


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']
    inlines = [CityAdminInline]


# Admin for City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'province_name']
    search_fields = ['name']

    @admin.display(ordering=['province_name'])
    def province_name(self, city: City):
        return city.province.name
    province_name.short_description = _("Province Name")


class ProfitStatementInline(admin.StackedInline):
    model = ProfitLossStatement
    extra = 0
    min_num = 1
    max_num = 1


class LifeCycleInline(admin.StackedInline):
    model = LifeCycle
    extra = 0
    min_num = 1
    max_num = 1


class SaledProductInline(admin.StackedInline):
    model = SoldProductFee
    extra = 0
    min_num = 1
    max_num = 1


class BalanceReportInline(admin.StackedInline):
    model = BalanceReport
    extra = 0
    min_num = 1
    max_num = 1


class TaxDeclarationInline(admin.StackedInline):
    model = TaxDeclarationFile
    extra = 0
    min_num = 1
    max_num = 1


class AccountTurnOverInline(admin.StackedInline):
    model = AccountTurnOver
    extra = 0
    min_num = 1
    max_num = 1


@admin.register(FinancialAsset)
class FinancialAssestModel(admin.ModelAdmin):
    list_display = ['company__company_title', 'year']
    inlines = [TaxDeclarationInline, BalanceReportInline, ProfitStatementInline, SaledProductInline,
               AccountTurnOverInline]
    # This will allow selection of multiple life cycles
    filter_horizontal = ('capital_providing_method',)


@admin.register(LifeCycle)
class LifeCycleAdmin(admin.ModelAdmin):
    list_display = ['capital_providing', 'other_capital_providing']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    pass


@admin.register(CompanyService)
class CompanyServiceAdmin(admin.ModelAdmin):
    pass


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    pass
