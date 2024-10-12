from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import User
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
