import logging


from django.contrib.auth.models import BaseUserManager as BaseManager


logger = logging.getLogger("core")


class UserManager(BaseManager):
    def create_user(self, phone_number, national_code=None, password=None, **kwargs):
        if not phone_number:
            logger.error("User creation failed: phone number is missing")
            raise ValueError("The phone number must be set")

        if not national_code:
            logger.error("User creation failed: national code is missing")
            raise ValueError("The national code must be set")

        user = self.model(
            phone_number=phone_number, national_code=national_code, **kwargs
        )

        if password:
            user.set_password(password)
            logger.info(f"Setting password for user with phone: {phone_number}")

        else:
            user.set_unusable_password()
            logger.warning(f"User with phone {phone_number} has an unusable password")

        user.save(using=self._db)
        logger.info(f"User created successfully: {phone_number}")
        return user

    def create_superuser(self, phone_number, national_code, password=None, **kwargs):
        kwargs.setdefault("is_active", True)
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)

        if not password:
            logger.error("Superuser creation failed: missing password")
            raise ValueError("Superusers must have a password")

        logger.info(f"Creating superuser with phone: {phone_number}")
        return self.create_user(
            phone_number=phone_number,
            national_code=national_code,
            password=password,
            **kwargs,
        )
