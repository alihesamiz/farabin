from django.contrib.auth.models import BaseUserManager as BaseManager


class UserManager(BaseManager):

    def create_user(self, phone_number, national_code=None, password=None, **kwargs):
        if not phone_number:
            raise ValueError("The phone number must be set")

        if not national_code:
            raise ValueError("The national code must be set")

        user = self.model(phone_number=phone_number,
                          national_code=national_code, **kwargs)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, national_code, password=None, **kwargs):
        kwargs.setdefault('is_active', True)
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)

        if not password:
            raise ValueError('Superusers must have a password')

        return self.create_user(phone_number=phone_number, national_code=national_code, password=password, **kwargs)
