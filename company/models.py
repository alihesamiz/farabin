from core.utils import GeneralUtils
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from uuid import uuid4

# Create your models here.


User = get_user_model()


####################################
"""Life Cycle"""


class LifeCycle(models.Model):
    OPERATIONAL = 'operational'
    FINANCE = 'finance'
    INVEST = 'invest'

    LIFE_CYCLE_CHOICES = [
        (OPERATIONAL, _('Operational')),
        (FINANCE, _('Finance')),
        (INVEST, _('Invest')),
    ]
    capital_providing = models.CharField(
        max_length=11, choices=LIFE_CYCLE_CHOICES, default=OPERATIONAL, verbose_name=_("Capital Providing"))

    class Meta:
        verbose_name = _('Life Cycle')
        verbose_name_plural = _('Life Cycles')

    def __str__(self):
        return self.get_capital_providing_display()


####################################
"""Special tech Model"""


class SpecialTech(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Name"))

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = _("Special Tech")
        verbose_name_plural = _("Special Techs")


####################################
"""tech field Model"""


class TechField(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Name"))

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = _("Tech Field")
        verbose_name_plural = _("Tech Fields")


####################################
"""Company Model"""


class CompanyProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    NEWBIE_LICENSE = 'n'
    INNOVATIVE_LICENSE = 'i'
    TECHNOLOGICAL_LICENSE = 'l'
    LICENSE_CHOICES = [
        (NEWBIE_LICENSE, _("Newbie")),
        (INNOVATIVE_LICENSE, _("Innovative")),
        (TECHNOLOGICAL_LICENSE, _("Technological")),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='company', verbose_name=_("User"))

    profile_active = models.BooleanField(
        default=False, verbose_name=_("Profile Active"))

    company_title = models.CharField(
        max_length=255, verbose_name=_("Company Title"))

    email = models.EmailField(
        max_length=255, unique=True, verbose_name=_("Email"))

    social_code = models.CharField(
        max_length=10, unique=True, verbose_name=_("Social Code"))

    manager_name = models.CharField(
        max_length=255, verbose_name=_("Manager Full Name"))

    license = models.CharField(
        max_length=1, choices=LICENSE_CHOICES, verbose_name=_("License Type"))

    tech_field = models.ForeignKey('TechField', default=1,
                                   on_delete=models.CASCADE,
                                   verbose_name=_("Technical Field"))

    special_field = models.ForeignKey('SpecialTech', default=1,
                                      on_delete=models.CASCADE,
                                      verbose_name=_("Special Field")
                                      )

    insurance_list = models.PositiveSmallIntegerField(
        default=1, verbose_name=_("Insurance List"))

    # organization = models.ForeignKey(
    #     'core.Organization', null=True, blank=True, verbose_name=_("Organization"), on_delete=models.CASCADE)

    capital_providing_method = models.ManyToManyField(
        LifeCycle, verbose_name=_('Capital Providing Method'), related_name='company_profile')

    province = models.ForeignKey(
        'core.Province', default=1, on_delete=models.CASCADE, verbose_name=_("Province"))

    city = models.ForeignKey(
        'core.City', default=1, on_delete=models.CASCADE, verbose_name=_("City"))

    address = models.CharField(max_length=255, verbose_name=_("Address"))

    class Meta:
        verbose_name = _("Company Profile")
        verbose_name_plural = _("Company Profiles")

    def __str__(self) -> str:
        return f"{self.company_title} - {self.user.national_code}"


####################################
"""Company service"""


class CompanyService(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE,
                                related_name='services', verbose_name=_("Company"))
    service = models.ForeignKey(
        'core.Service', on_delete=models.CASCADE, verbose_name=_("Service"))
    is_active = models.BooleanField(default=False, verbose_name=_("Activate"))
    purchased_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Purchased Date"))

    class Meta:
        unique_together = ("company", "service")
        verbose_name = _("Company Service")
        verbose_name_plural = _("Company Services")

    def __str__(self) -> str:
        return f"{self.company.company_title} - {self.service.name} ({'Active' if self.is_active else 'Inactive'})"


####################################
"""Dashboard Model"""


class Dashboard(models.Model):
    company_service = models.ForeignKey(
        CompanyService, on_delete=models.CASCADE, related_name='dashboards', verbose_name=_("Company Service"))

    class Meta:
        verbose_name = _("Dashboard")
        verbose_name_plural = _("Dashboards")

    def __str__(self) -> str:
        return f"Dashboard for {self.company_service.company.company_title} - {self.company_service.service.name}"


TAX_FILE_UPLOADING_PATH = GeneralUtils(
    path="financial_files/files/tax_files",
    fields=['company__company_title', 'year']
)


####################################
"""TaxDeclaration Model"""


class TaxDeclaration(models.Model):

    company = models.ForeignKey(CompanyProfile, on_delete=models.SET_NULL, null=True, verbose_name=_(
        "Company"), related_name="taxfiles")

    year = models.PositiveSmallIntegerField()

    tax_file = models.FileField(verbose_name=_(
        "File"), upload_to=TAX_FILE_UPLOADING_PATH.rename_folder, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.company.company_title} -> {self.year}"

    class Meta:
        verbose_name = _("Tax Declaration")
        verbose_name_plural = _("Tax Declarations")
        unique_together = [['company', 'year']]


########################
"""non-TaxDeclaration Model"""

BALANCE_REPORT_FILE_UPLOADING_PATH = GeneralUtils(
    path="financial_files/files/non-tax_files",
    fields=['company__company_title', 'year']
)


class BalanceReport(models.Model):

    company = models.ForeignKey(CompanyProfile, on_delete=models.SET_NULL, null=True, verbose_name=_(
        "Company"), related_name="reportfiles")

    year = models.PositiveSmallIntegerField()

    balance_report_file = models.FileField(verbose_name=_(
        "Balance Report File"), upload_to=BALANCE_REPORT_FILE_UPLOADING_PATH.rename_folder, blank=True, null=True)

    prift_loss_file = models.FileField(verbose_name=_(
        "Prift Loss File"), upload_to=BALANCE_REPORT_FILE_UPLOADING_PATH.rename_folder, blank=True, null=True)

    sold_product_file = models.FileField(verbose_name=_(
        "Sold Product File"), upload_to=BALANCE_REPORT_FILE_UPLOADING_PATH.rename_folder, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.company.company_title} -> {self.year}"

    class Meta:
        verbose_name = _("Balance Report")
        verbose_name_plural = _("Balance Reports")
        unique_together = [['company', 'year']]
