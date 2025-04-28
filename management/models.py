from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db import models


from core.validators import excel_file_validator
from core.utils import GeneralUtils


def get_hr_file_upload_path(instance, filename):
    path = GeneralUtils(
        path="hr_files", fields=['']).rename_folder(instance, filename)
    return path


class HumanResource(models.Model):
    company = models.ForeignKey('company.CompanyProfile', verbose_name=_(
        "Company"), null=False, blank=False, on_delete=models.CASCADE, related_name="hrfiles")

    excel_file = models.FileField(verbose_name=_(
        "Excel File"), blank=False, null=False, upload_to=get_hr_file_upload_path, validators=[excel_file_validator])

    is_approved = models.BooleanField(
        verbose_name=_("Is Approved"), default=False)

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Updated At"))

    def __str__(self):
        return f"{self.company.company_title}"  # › {self.excel_file}"

    class Meta:
        verbose_name = _("Human Resource")
        verbose_name_plural = _("Human Resources")
        constraints = [
            models.UniqueConstraint(
                fields=['company'], name='unique_company_hr')
        ]


class PersonelInformation(models.Model):
    human_resource = models.ForeignKey(HumanResource, verbose_name=_(
        "Human Resource"), null=False, blank=False, on_delete=models.CASCADE, related_name='personelinformation')

    name = models.CharField(verbose_name=_("Full Name"),
                            max_length=250, null=False, blank=False)

    position = models.CharField(verbose_name=_(
        "Position"), max_length=150, null=False, blank=False)

    reports_to = models.ManyToManyField('self', verbose_name=_(
        "Reports to (Personnel)"), blank=True)

    cooperates_with = models.ManyToManyField('self', verbose_name=_(
        "Cooperates with (Personnel)"), blank=True)

    obligations = models.TextField(verbose_name=_(
        "Obligation"), null=False, blank=False)

    is_exist = models.BooleanField(
        verbose_name=_("Is Exist"),
        default=False
    )

    class Meta:
        verbose_name = _("Personnel Information")
        verbose_name_plural = _("Personnel Information")

    def __str__(self):
        return f"{self.name}"

    @classmethod
    def grouped_chart_data(cls, company):
        queryset = cls.objects.prefetch_related(
            "human_resource__company").filter(human_resource__company=company)
        grouped_data = {}

        for person in queryset:
            pos = person.position
            name = person.name
            key = (pos, name)

            if key not in grouped_data:
                grouped_data[key] = {
                    'personnel': [],
                    'aggregated_reports_to': set(),
                    'aggregated_cooperates_with': set()
                }
            grouped_data[key]['personnel'].append(person.position)

            if person.reports_to.exists():
                for report in person.reports_to.all():
                    grouped_data[key]['aggregated_reports_to'].add(
                        (report.position, report.name)
                    )

            if person.cooperates_with.exists():
                for cooperate in person.cooperates_with.all():
                    grouped_data[key]['aggregated_cooperates_with'].add(
                        (cooperate.position, cooperate.name)
                    )

        response_data = {}
        for (pos, name), data in grouped_data.items():
            response_data[f"{pos} | {name}"] = {
                'aggregated_reports_to': [
                    {'position': position, 'name': report_name} for position, report_name in data['aggregated_reports_to']
                ],
                'aggregated_cooperates_with': [
                    {'position': position, 'name': cooperate_name} for position, cooperate_name in data['aggregated_cooperates_with']
                ]
            }

        return response_data


def get_chart_excel_file_upload_path(instance, filename):
    path = GeneralUtils(
        path="chart_excel_files", fields=['field']).rename_folder(instance, filename)
    return path


class OrganizationChartBase(models.Model):

    field = models.CharField(verbose_name=_(
        "Field"), max_length=150, null=False, blank=False)

    position_excel = models.FileField(verbose_name=_("Position Excel"), max_length=150, null=False, blank=False,
                                      upload_to=get_chart_excel_file_upload_path, validators=[excel_file_validator])

    def __str__(self):
        return f"{self.field.title()}"

    class Meta:
        verbose_name = _("Organization Chart")
        verbose_name_plural = _("Organization Charts")


COMMON_SWOT_CHOICES = [
    ('strong', _('Strong')),
    ('weak', _('Weak')),
    ('average', _('Average')),
    ('excellent', _('Excellent')),
    ('good', _('Good')),
    ('poor', _('Poor')),
    ('satisfactory', _('Satisfactory')),
    ('unsatisfactory', _('Unsatisfactory')),
]


class SWOTOption(models.Model):
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=100,
        choices=COMMON_SWOT_CHOICES,
        blank=True,
        null=True,
    )
    custom_name = models.CharField(
        verbose_name=_("Custom Name"),
        max_length=100,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        if self.custom_name:
            return self.custom_name
        if self.name:
            return self.get_name_display()
        return "Unnamed"

    def clean(self):
        errors = {}
        if not self.name and not self.custom_name:
            errors['name'] = _(
                "Either a predefined name or a custom name must be provided.")
            errors['custom_name'] = _(
                "Either a predefined name or a custom name must be provided.")
        if self.name and self.custom_name:
            errors['name'] = _(
                "Cannot provide both a predefined name and a custom name.")
            errors['custom_name'] = _(
                "Cannot provide both a predefined name and a custom name.")
        if self.custom_name and not self.custom_name.strip():
            errors['custom_name'] = _("Custom name cannot be empty.")

        if errors:
            raise ValidationError(errors)

    @classmethod
    def generate_constraints(cls, prefix: str):
        return [
            models.UniqueConstraint(
                fields=['name'],
                condition=models.Q(name__isnull=False),
                name=f'unique_{prefix}_name'
            ),
            models.UniqueConstraint(
                fields=['custom_name'],
                condition=models.Q(custom_name__isnull=False),
                name=f'unique_{prefix}_custom_name'
            ),
        ]


class SWOTStrengthOption(SWOTOption):

    class Meta:
        verbose_name = _("SWOT Strength Option")
        verbose_name_plural = _("SWOT Strengths Option")
        # Adding unique constraints to ensure that either name or custom_name is unique
        constraints = SWOTOption.generate_constraints('strength')


class SWOTWeaknessOption(SWOTOption):

    class Meta:
        verbose_name = _("SWOT Weakness Option")
        verbose_name_plural = _("SWOT Weaknesses Option")
        # Adding unique constraints to ensure that either name or custom_name is unique
        constraints = SWOTOption.generate_constraints('weakness')


class SWOTOpportunityOption(SWOTOption):

    class Meta:
        verbose_name = _("SWOT Opportunity Option")
        verbose_name_plural = _("SWOT Opportunities Option")
        # Adding unique constraints to ensure that either name or custom_name is unique
        constraints = SWOTOption.generate_constraints('opportunity')


class SWOTThreatOption(SWOTOption):

    class Meta:
        verbose_name = _("SWOT Threat Option")
        verbose_name_plural = _("SWOT Threats Option")
        # Adding unique constraints to ensure that either name or custom_name is unique
        constraints = SWOTOption.generate_constraints('threat')


class SWOTMatrix(models.Model):
    company = models.ForeignKey(
        'company.CompanyProfile',
        verbose_name=_("Company"),
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="swot_matrices"
    )

    strengths = models.ManyToManyField(
        SWOTStrengthOption,
        verbose_name=_("Strengths Options"),
        related_name="swot_matrices_strengths"
    )
    weaknesses = models.ManyToManyField(
        SWOTWeaknessOption,
        verbose_name=_("Weaknesses Options"),
        related_name="swot_matrices_weaknesses"
    )
    opportunities = models.ManyToManyField(
        SWOTOpportunityOption,
        verbose_name=_("Opportunities Options"),
        related_name="swot_matrices_opportunities"
    )
    threats = models.ManyToManyField(
        SWOTThreatOption,
        verbose_name=_("Threats Options"),
        related_name="swot_matrices_threats"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At")
    )

    class Meta:
        verbose_name = _("SWOT Matrix")
        verbose_name_plural = _("SWOT Matrices")
        constraints = [
            models.UniqueConstraint(
                fields=['company'],
                name='unique_company_swot'
            )
        ]

    def __str__(self):
        return f"{self.company.company_title!r} SWOT"


class SWOTAnalysis(models.Model):
    swot_matrix = models.ForeignKey(
        SWOTMatrix,
        verbose_name=_("SWOT Matrix"),
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="swot_analysis"
    )

    so_analysis = models.TextField(
        verbose_name=_("SO Analysis"),
        null=True,
        blank=True
    )
    st_analysis = models.TextField(
        verbose_name=_("ST Analysis"),
        null=True,
        blank=True
    )
    wo_analysis = models.TextField(
        verbose_name=_("WO Analysis"),
        null=True,
        blank=True
    )
    wt_analysis = models.TextField(
        verbose_name=_("WT Analysis"),
        null=True,
        blank=True
    )

    is_approved = models.BooleanField(
        verbose_name=_("Is Approved"),
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At")
    )

    class Meta:
        verbose_name = _("SWOT Analysis")
        verbose_name_plural = _("SWOT Analysis")
        constraints = [
            models.UniqueConstraint(
                fields=['swot_matrix'],
                name='unique_swot_analysis'
            )
        ]

    def __str__(self):
        return f"{self.swot_matrix.company.company_title!r} SWOT Analysis"
