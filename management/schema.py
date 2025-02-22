from django.core.exceptions import ObjectDoesNotExist


from graphene.types import List, Field, String, Int, ObjectType, JSONString, Mutation, Schema
from graphql_jwt import ObtainJSONWebToken, Verify, Refresh
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required


from management.models import HumanResource, PersonelInformation, OrganizationChartBase
from management.utils import get_file_field


class HumanResourceType(DjangoObjectType):
    class Meta:
        model = HumanResource
        fields = ("id", "excel_file", "company", "create_at", "updated_at")


class PersonelInformationType(DjangoObjectType):
    class Meta:
        model = PersonelInformation
        fields = ("id", "human_resource", "name",
                  "unit", "position", "reports_to")


class OrganizationChartType(DjangoObjectType):
    class Meta:
        model = OrganizationChartBase
        fields = ("id", "field", "position_excel")


class Query(ObjectType):

    human_resources = List(HumanResourceType)

    personel_informations = List(
        PersonelInformationType,
        human_resource_id=Int()
    )

    organization_charts = List(OrganizationChartType)

    chart_nodes = Field(JSONString)

    @login_required
    def resolve_human_resources(self, info, **kwargs):
        user = info.context.user
        company = user.company
        return HumanResource.objects.filter(company=company)

    @login_required
    def resolve_personel_informations(self, info, human_resource_id=None, **kwargs):
        user = info.context.user
        company = user.company
        if human_resource_id:
            return PersonelInformation.objects.filter(
                human_resource__id=human_resource_id,
                human_resource__company=company
            )
        return PersonelInformation.objects.none()

    @login_required
    def resolve_organization_charts(self, info, **kwargs):
        user = info.context.user

        tech_field = user.company.tech_field
        file_field = get_file_field(tech_field)
        return OrganizationChartBase.objects.filter(field=file_field)

    @login_required
    def resolve_chart_nodes(self, info, **kwargs):
        """
        This resolver groups PersonelInformation by their position,
        and aggregates the reports-to positions.
        """
        user = info.context.user
        company = user.company
        queryset = PersonelInformation.objects.filter(
            human_resource__company=company)
        grouped_data = {}

        for person in queryset:
            pos = person.position
            if pos not in grouped_data:
                grouped_data[pos] = {
                    'personnel': [],
                    'aggregated_reports_to': set()
                }
            grouped_data[pos]['personnel'].append({
                'id': person.id,
                'name': person.name,
                'unit': person.unit,
                'position': person.position,
                'reports_to': person.reports_to.id if person.reports_to else None
            })
            if person.reports_to:
                grouped_data[pos]['aggregated_reports_to'].add(
                    person.reports_to.position)

        for pos in grouped_data:
            grouped_data[pos]['aggregated_reports_to'] = list(
                grouped_data[pos]['aggregated_reports_to'])

        return grouped_data


class CreateHumanResource(Mutation):
    human_resource = Field(HumanResourceType)

    class Arguments:
        excel_file = String(required=True)

    @login_required
    def mutate(self, info, excel_file):
        user = info.context.user
        company = user.company

        if HumanResource.objects.filter(company=company).exists():
            raise Exception(
                "Each company can only have one Human Resource record. Delete the existing record first.")

        hr = HumanResource(excel_file=excel_file, company=company)
        hr.save()
        return CreateHumanResource(human_resource=hr)


class UpdateHumanResource(Mutation):
    human_resource = Field(HumanResourceType)

    class Arguments:
        id = Int(required=True)
        excel_file = String(required=False)

    @login_required
    def mutate(self, info, id, excel_file=None):
        user = info.context.user
        company = user.company

        try:
            hr = HumanResource.objects.get(id=id, company=company)
        except ObjectDoesNotExist:
            raise Exception("HumanResource not found for your company.")

        if excel_file is not None:
            hr.excel_file = excel_file
        hr.save()
        return UpdateHumanResource(human_resource=hr)


class CreatePersonelInformation(Mutation):
    personel_information = Field(PersonelInformationType)

    class Arguments:
        human_resource_id = Int(required=True)
        name = String(required=True)
        unit = String(required=True)
        position = String(required=True)
        reports_to_id = Int(required=False)

    @login_required
    def mutate(self, info, human_resource_id, name, unit, position, reports_to_id=None):
        user = info.context.user
        company = user.company

        try:
            hr = HumanResource.objects.get(
                id=human_resource_id, company=company)
        except ObjectDoesNotExist:
            raise Exception("HumanResource record not found for your company.")

        reports_to = None
        if reports_to_id:
            try:
                reports_to = PersonelInformation.objects.get(
                    id=reports_to_id, human_resource__company=company)
            except ObjectDoesNotExist:
                raise Exception("Invalid 'reports_to' reference.")

        person = PersonelInformation.objects.create(
            human_resource=hr,
            name=name,
            unit=unit,
            position=position,
            reports_to=reports_to
        )
        return CreatePersonelInformation(personel_information=person)


class UpdatePersonelInformation(Mutation):
    personel_information = Field(PersonelInformationType)

    class Arguments:
        id = Int(required=True)
        name = String(required=False)
        unit = String(required=False)
        position = String(required=False)
        reports_to_id = Int(required=False)

    @login_required
    def mutate(self, info, id, name=None, unit=None, position=None, reports_to_id=None):
        user = info.context.user
        company = user.company

        try:
            person = PersonelInformation.objects.get(
                id=id, human_resource__company=company)
        except ObjectDoesNotExist:
            raise Exception(
                "Personnel Information not found for your company.")

        if name is not None:
            person.name = name
        if unit is not None:
            person.unit = unit
        if position is not None:
            person.position = position
        if reports_to_id is not None:
            try:
                reports_to = PersonelInformation.objects.get(
                    id=reports_to_id, human_resource__company=company)
            except ObjectDoesNotExist:
                raise Exception("Invalid 'reports_to' reference.")
            person.reports_to = reports_to

        person.save()
        return UpdatePersonelInformation(personel_information=person)


class Mutation(ObjectType):

    create_human_resource = CreateHumanResource.Field()
    update_human_resource = UpdateHumanResource.Field()

    create_personel_information = CreatePersonelInformation.Field()
    update_personel_information = UpdatePersonelInformation.Field()

    token_auth = ObtainJSONWebToken.Field()
    verify_token = Verify.Field()
    refresh_token = Refresh.Field()


schema = Schema(query=Query, mutation=Mutation)
