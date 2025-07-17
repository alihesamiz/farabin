from apps.company.repositories import CompanyRepository as _repo
from apps.company.models import CompanyUser


class CompanyService:
    @staticmethod
    def add_user_to_company(
        company, validated_data: dict, role: str = CompanyUser.Role.STAFF
    ):
        """
        Add a user to the given company. Creates a user if one does not exist.
        """
        phone_number = validated_data["phone_number"]

        # Get or create user
        user, created = _repo.get_or_create_user(phone_number, defaults=validated_data)

        if not created:
            raise ValueError("User already exists!")

        # Create company user
        company_user = _repo.create_company_user(user, company, role)
        return company_user
