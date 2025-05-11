from getpass import getpass
import os


from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext_lazy as _
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Create a staff user and assign specific permissions"

    def handle(self, *args, **kwargs):
        phone_number = None
        national_code = None
        password = None

        while not phone_number:
            phone_number = input("Phone number: ")
            if User.objects.filter(phone_number=phone_number).exists():
                self.stderr.write(
                    self.style.ERROR(
                        f"User with phone number {phone_number} already exists."
                    )
                )
                phone_number = None

        while not national_code:
            national_code = input("National code: ")
            if User.objects.filter(national_code=national_code).exists():
                self.stderr.write(
                    self.style.ERROR(
                        f"User with national code {national_code} already exists."
                    )
                )
                national_code = None

        while password is None:
            password = self.get_password()

        user = User.objects.create_user(
            phone_number=phone_number, national_code=national_code, password=password
        )
        user.is_staff = True
        user.save()

        group_name = input('Group (leave blank for default "Editor"): ') or _("Editor")

        try:
            group, created = Group.objects.get_or_create(name=group_name)

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Group "{group_name}" created successfully.')
                )

                try:

                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    file_path = os.path.join(script_dir, "staff_permissions.txt")
                    with open(file_path, "r") as file:
                        for line in file:
                            codename = line.strip()
                            try:
                                permission = Permission.objects.filter(
                                    codename=codename
                                ).first()
                                if permission:
                                    group.permissions.add(permission)
                                    self.stdout.write(
                                        self.style.SUCCESS(
                                            f'Permission "{codename}" added to group "{group_name}".'
                                        )
                                    )
                                else:
                                    self.stderr.write(
                                        self.style.ERROR(
                                            f'Permission "{codename}" does not exist.'
                                        )
                                    )
                            except Exception as e:
                                self.stderr.write(
                                    self.style.ERROR(
                                        f'Error adding permission "{codename}": {str(e)}'
                                    )
                                )
                except FileNotFoundError:
                    self.stderr.write(
                        self.style.ERROR(
                            "Permissions file not found. No permissions were added."
                        )
                    )

            else:
                self.stdout.write(
                    self.style.SUCCESS(f'Group "{group_name}" already exists.')
                )

            user.groups.add(group)

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred: {str(e)}"))

    def get_password(self):
        password = getpass("Password: ")
        password2 = getpass("Password (again): ")
        if password != password2:
            self.stderr.write(self.style.ERROR("Passwords do not match."))
            return None
        if len(password) < 8:
            self.stderr.write(
                self.style.ERROR(
                    "Password too short. It must be at least 8 characters long."
                )
            )
            return None
        return password
