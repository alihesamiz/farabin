from django.conf import settings

from apps.management.models import (
    HumanResource,
    OrganizationChartBase,
    PersonelInformation,
    Position,
)
from constants.typing import CompanyProfileType, UserType


class ManagementRepository:
    def get_company(user: UserType):
        return user.company_user.company

    def check_query_set_exists(qs):
        return qs if qs.exists() else qs.none()

    def get_tech_field_file(field):
        """Returns the existing file based on the company given field"""
        from apps.company.models import TechField

        REVERSED_TECH_FIELDS = {
            field: key
            for key, fields in settings.HUMAN_RESOURCE_FILE_FIELDS.items()
            for field in [
                (
                    sub_field
                    if sub_field != "__all__"
                    else list(TechField.objects.values_list("name", flat=True))
                )
                for sub_field in fields
            ][0]
        }
        file_field = REVERSED_TECH_FIELDS[str(field)]

        return file_field

    @classmethod
    def get_human_resource_record_of_company(cls, company: CompanyProfileType):
        qs = HumanResource.objects.select_related("company").filter(company=company)
        return cls.check_query_set_exists(qs)

    @classmethod
    def get_personnel_info_of_company(cls, company: CompanyProfileType):
        qs = (
            PersonelInformation.objects.select_related("human_resource")
            .prefetch_related(
                "reports_to",
                "cooperates_with",
                "human_resource__company",
            )
            .filter(human_resource__company=company)
        )
        return cls.check_query_set_exists(qs)

    @classmethod
    def get_personnel_info_grouped_chart_data(cls, company: CompanyProfileType):
        """
        This functions gather the data for each person with the aggregated
        'reports-to' and 'cooperates-with' values
        """
        queryset = cls.get_personnel_info_of_company(company)
        grouped_data = {}

        for person in queryset:
            pos = person.position
            name = person.name
            key = (pos, name)

            if key not in grouped_data:
                grouped_data[key] = {
                    "personnel": [],
                    "aggregated_reports_to": set(),
                    "aggregated_cooperates_with": set(),
                }
            grouped_data[key]["personnel"].append(person.position)

            if person.reports_to.exists():
                for report in person.reports_to.all():
                    grouped_data[key]["aggregated_reports_to"].add(
                        (report.position, report.name)
                    )

            if person.cooperates_with.exists():
                for cooperate in person.cooperates_with.all():
                    grouped_data[key]["aggregated_cooperates_with"].add(
                        (cooperate.position, cooperate.name)
                    )

        response_data = {}
        for (pos, name), data in grouped_data.items():
            response_data[f"{pos} | {name}"] = {
                "aggregated_reports_to": [
                    {"position": position, "name": report_name}
                    for position, report_name in data["aggregated_reports_to"]
                ],
                "aggregated_cooperates_with": [
                    {"position": position, "name": cooperate_name}
                    for position, cooperate_name in data["aggregated_cooperates_with"]
                ],
            }

        return response_data

    @classmethod
    def get_personnel_info_by_position(cls, qs, serializer, positions):
        """
        Group personnel by position.
        """
        queryset = qs.filter(position__in=positions)

        grouped_personnel = {}
        for person in queryset:
            pos = person.position
            grouped_personnel.setdefault(pos, []).append(serializer(person).data)

        return grouped_personnel

    @classmethod
    def get_position_by_code(code: int):
        try:
            return Position.objects.get(code=code).position
        except Exception:
            raise Exception(f"No position found with the given code {code}")

    @classmethod
    def get_base_chart_file_of_company(cls, company: CompanyProfileType):
        
        if not company:
            return OrganizationChartBase.objects.none()

        field = getattr(company, "tech_field", None)
        if not field:
            return OrganizationChartBase.objects.none()

        file_field = cls.get_tech_field_file(field)
        if not file_field:
            return OrganizationChartBase.objects.none()
            