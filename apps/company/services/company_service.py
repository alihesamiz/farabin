from apps.company.models import CompanyProfile, CompanyUser
from apps.company.repositories import CompanyRepository as _repo
from constants.typing import CompanyProfileType, CompanyUserType, UserType


class CompanyService:
    @staticmethod
    def create_company_user(
        user: UserType, company: CompanyProfileType, role: str = CompanyUser.Role.STAFF
    ) -> CompanyUserType:
        """
        Create a CompanyUser entry linking user to company.
        """
        return CompanyUser.objects.create(user=user, company=company, role=role)

    @classmethod
    def add_user_to_company(
        cls,
        company: CompanyProfileType,
        validated_data: dict,
        role: str = CompanyUser.Role.STAFF,
    ) -> CompanyUserType:
        """
        Add a user to the given company. Creates a user if one does not exist.
        """
        phone_number = validated_data["phone_number"]

        user, created = _repo.get_or_create_user(phone_number, defaults=validated_data)

        if not created:
            raise ValueError("User already exists!")

        company_user = cls.create_company_user(user, company, role)
        return company_user

    @classmethod
    def create_profile_for_user(cls, user: UserType) -> CompanyProfileType:
        company = CompanyProfile.objects.create()
        cls.create_company_user(user, company, CompanyUser.Role.MANAGER)
        return company
