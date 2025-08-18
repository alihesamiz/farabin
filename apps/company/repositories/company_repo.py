from django.contrib.auth import get_user_model

from apps.company.models import CompanyProfile, CompanyUser
from constants.typing import Any, Optional, QuerySet, Tuple, UserType

User = get_user_model()


class CompanyRepository:
    """
    A repository for handling company-related database operations.
    """

    @staticmethod
    def get_company_for_user(user: UserType) -> Optional[QuerySet[CompanyProfile]]:
        """
        Retrieves the company profiles associated with a given user.
        """
        try:
            return (
                CompanyProfile.objects.select_related(
                    "tech_field",
                    "special_field",
                    "province",
                    "city",
                )
                .prefetch_related(
                    "license",
                    "capital_providing_method",
                )
                .filter(company_user__user=user)
                .distinct()
            )
        except CompanyProfile.DoesNotExist:
            # Note: A .filter() call will not raise DoesNotExist.
            # It will return an empty QuerySet. This try/except
            # block might be for a .get() call elsewhere.
            # Returning None here is kept to match the original code's intent.
            return None

    @staticmethod
    def get_company_user_for_company(
        company: CompanyProfile, not_deleted: bool = True
    ) -> QuerySet[CompanyUser]:
        """
        Retrieves the company users for a given company.
        """
        return CompanyUser.objects.select_related(
            "user",
            "company",
        ).filter(company=company, deleted_at__isnull=not_deleted)

    @staticmethod
    def get_or_create_user(
        phone_number: str, defaults: dict[str, Any]
    ) -> Tuple[UserType, bool]:
        """
        Get a user by phone number, or create one if it does not exist.
        Returns a tuple of (user_object, created_boolean).
        """
        return User.objects.get_or_create(
            phone_number=phone_number, defaults=defaults
        )
