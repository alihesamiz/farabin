from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import CommandError
from django.core.exceptions import ValidationError
from getpass import getpass

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a staff user and assign specific permissions'

    def handle(self, *args, **kwargs):
        phone_number = None
        national_code = None
        password = None

        # Prompt for phone number
        while not phone_number:
            phone_number = input('Phone number: ')
            if User.objects.filter(phone_number=phone_number).exists():
                self.stderr.write(self.style.ERROR(
                    f'User with phone number {phone_number} already exists.'))
                phone_number = None

        # Prompt for national code
        while not national_code:
            national_code = input('National code: ')
            if User.objects.filter(national_code=national_code).exists():
                self.stderr.write(self.style.ERROR(
                    f'User with national code {national_code} already exists.'))
                national_code = None

        # Prompt for password
        while password is None:
            password = self.get_password()

        # Create the staff user
        user = User.objects.create_user(
            phone_number=phone_number, national_code=national_code, password=password)
        user.is_staff = True
        user.save()

        # Prompt for group assignment
        group_name = input(
            'Group (leave blank for default "Editor"): ') or 'Editor'

        try:
            # Try to get the group by name
            group, created = Group.objects.get_or_create(name=group_name)
            group.permissions
            user.groups.add(group)
        except Group.DoesNotExist:
            self.stderr.write(self.style.ERROR(
                f'Group {group_name} does not exist.'))
            return

        # Assign permissions to view users (for Editor or other groups)
        try:
            user_ct = ContentType.objects.get_for_model(User)
            view_user_permission = Permission.objects.get(
                codename='view_user', content_type=user_ct)

            # Add 'view_user' permission to the user's group
            group.permissions.add(view_user_permission)

            self.stdout.write(
                self.style.SUCCESS(f'Successfully created staff user {phone_number}, added to {group_name}, and granted view user permission.'))

        except Permission.DoesNotExist:
            self.stderr.write(self.style.ERROR(
                f'Permission "view_user" does not exist.'))

    def get_password(self):
        password = getpass('Password: ')
        password2 = getpass('Password (again): ')
        if password != password2:
            self.stderr.write(self.style.ERROR('Passwords do not match.'))
            return None
        if len(password) < 8:
            self.stderr.write(self.style.ERROR(
                'Password too short. It must be at least 8 characters long.'))
            return None
        return password
