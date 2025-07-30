from uuid import uuid4

from apps.company.models import CompanyProfile, CompanyUser
from apps.company.repositories import CompanyRepository as _repo


class CompanyService:
    @staticmethod
    def create_company_user(user, company, role: str = CompanyUser.Role.STAFF):
        """
        Create a CompanyUser entry linking user to company.
        """
        return CompanyUser.objects.create(user=user, company=company, role=role)

    @classmethod
    def add_user_to_company(
        cls, company, validated_data: dict, role: str = CompanyUser.Role.STAFF
    ):
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
    def create_profile_for_user(cls, user):
        placeholder_title = f"Company-{uuid4().hex[:6]}"
        placeholder_code = f"{uuid4().int % 10**11:011d}"

        company = CompanyProfile.objects.create(
            title=placeholder_title,
            national_code=placeholder_code,
            address="(To be updated)",
            tech_field_id=1,
            special_field_id=1,
            province_id=1,
            city_id=1,
            insurance_list=1,
        )
        cls.create_company_user(user, company, CompanyUser.Role.MANAGER)
        return company
