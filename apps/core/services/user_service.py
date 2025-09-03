from django.db import IntegrityError  # type: ignore

from apps.core.models import User
from apps.company.models import CompanyUser, CompanyProfile
from apps.core.repositories import UserRepository as _user_repo
from constants.errors.api_exception import (
    InvalidCredentialsError,
    PasswordMismatchError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from constants.typing import CompanyProfileType, UserType


class UserService:
    @staticmethod
    def create_user_with_phone_number(phone_number: str, social_code: str) -> UserType:
        try:
            user =  User.objects.create_user(
                phone_number=phone_number, social_code=social_code, password=None
            )

            company_profile = CompanyProfile.objects.create()

            company_user = CompanyUser.objects.create(
                user=user,
                company=company_profile,  # Assuming company can be null initially
            )   

            user.save()
            company_profile.save()
            company_user.save()
            
            return user
        
        except IntegrityError:
            raise UserAlreadyExistsError

    @staticmethod
    def check_user_password_returns_user(phone_number: str, password: str) -> UserType:
        try:
            user = _user_repo.get_user_by_phone_number(phone_number)
        except User.DoesNotExist:
            raise UserNotFoundError
        if not user.check_password(password):
            raise InvalidCredentialsError
        return user

    @classmethod
    def reset_user_password(cls, phone_number: str, cpwd: str, npwd: str, npwd1: str):
        user = cls.check_user_password_returns_user(phone_number, cpwd)

        if npwd != npwd1:
            raise PasswordMismatchError

        user.set_password(npwd1)
        user.save()

    @staticmethod
    def create_company_user(user): ...

    @staticmethod
    def create_company_returns_company(user) -> CompanyProfileType:
        from apps.company.services import CompanyService

        company = CompanyService.create_profile_for_user(user)
        return company
