from django.contrib.auth import get_user_model

from apps.company.models import CompanyProfile, CompanyUser

User = get_user_model()


class CompanyRepository:
    @staticmethod
    def get_company_for_user(user):
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
            return None

    @staticmethod
    def get_company_user_for_company(company, not_deleted: bool = True):
        return CompanyUser.objects.select_related(
            "user",
            "company",
        ).filter(company=company,deleted_at__isnull=not_deleted)

    @staticmethod
    def get_or_create_user(phone_number: str, defaults: dict):
        """
        Get a user by phone number, or create one if it does not exist.
        """
        return User.objects.get_or_create(phone_number=phone_number, defaults=defaults)
