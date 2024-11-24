from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .models import Service

# Register your models here.

User = get_user_model()


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
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        (_('Important dates'), {'fields': ('last_login',)}),
    )

    # Define the fields to display when creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'national_code', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )

    # Fields that are read-only in the admin interface
    readonly_fields = ('last_login', 'password')

    # Remove filter_horizontal since 'groups' and 'user_permissions' do not exist
    filter_horizontal = ('groups', 'user_permissions')

    # Remove 'groups' from list_filter
    list_filter = ('is_active', 'is_staff', 'is_superuser')


# @admin.register(Institute)
# class InstituteAdmin(admin.ModelAdmin):
#     list_display = ['title', 'province']
#     autocomplete_fields = ['province']
#     search_fields = ['title']

# Admin for Province


# class CityAdminInline(admin.StackedInline):
#     model = City
#     extra = 0
#     min_num = 0


# @admin.register(Province)
# class ProvinceAdmin(admin.ModelAdmin):
#     list_display = ['name']
#     search_fields = ['name']
#     ordering = ['name']
#     inlines = [CityAdminInline]


# # Admin for City


# @admin.register(City)
# class CityAdmin(admin.ModelAdmin):
#     list_display = ['name', 'province_name']
#     search_fields = ['name']

#     @admin.display(ordering=['province_name'])
#     def province_name(self, city: City):
#         return city.province.name
#     province_name.short_description = _("Province Name")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'get_price', 'service_active']

    def get_price(self, service: Service):
        return f"{service.price:,.2f}"
    get_price.short_description = _("Price")
