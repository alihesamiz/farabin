from uuid import uuid4
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import models
from core.validators import pdf_file_validator
from core.utils import GeneralUtils
# Create your models here.


User = get_user_model()


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


class SpecialTech(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Name"))

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = _("Special Tech")
        verbose_name_plural = _("Special Techs")


class TechField(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Name"))

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = _("Tech Field")
        verbose_name_plural = _("Tech Fields")



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
        return f"{self.company_title} › {self.user.national_code}"



class CompanyService(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE,
                                related_name='services', verbose_name=_("Company"))
    service = models.ForeignKey(
        'core.Service', on_delete=models.CASCADE, verbose_name=_("Service"))
    is_active = models.BooleanField(default=False, verbose_name=_("Activate"))

    purchased_date = models.DateField(
        auto_now_add=True, verbose_name=_("Purchased Date"))

    class Meta:
        unique_together = ("company", "service")
        verbose_name = _("Company Service")
        verbose_name_plural = _("Company Services")

    def __str__(self) -> str:
        return f"{self.company.company_title} › {self.service.name} ({'Active' if self.is_active else 'Inactive'})"


class CompanyFileAbstract(models.Model):

    company = models.ForeignKey(CompanyProfile, on_delete=models.SET_NULL, null=True, verbose_name=_(
        "Company"))

    year = models.PositiveSmallIntegerField(verbose_name=_("Year"))

    is_saved = models.BooleanField(default=True, verbose_name=_("Is Saved"))

    is_sent = models.BooleanField(default=False, verbose_name=_("Is Sent"))

    class Meta:

        abstract = True


def get_tax_file_upload_path(instance, filename):
    path = GeneralUtils(path="tax_files", fields=[
                        'year']).rename_folder(instance, filename)
    return path


class TaxDeclaration(CompanyFileAbstract):

    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, null=True, verbose_name=_(
        "Company"), related_name="taxfiles")

    tax_file = models.FileField(verbose_name=_(
        "File"), upload_to=get_tax_file_upload_path, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.company.company_title} › {self.year}"

    class Meta:
        verbose_name = _("Tax Declaration")
        verbose_name_plural = _("Tax Declarations")
        unique_together = [['company', 'year']]


def get_non_tax_file_upload_path(instance, filename):
    path = GeneralUtils(
        path="non-tax_files", fields=['year', 'month']).rename_folder(instance, filename)
    return path


class BalanceReport(CompanyFileAbstract):

    MONTH_CHOICES = [(str(i), f"{i}") for i in range(1, 14)]

    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, null=True, verbose_name=_(
        "Company"), related_name="reportfiles")

    month = models.CharField(
        max_length=2, choices=MONTH_CHOICES, verbose_name=_("Month"))

    balance_report_file = models.FileField(verbose_name=_(
        "Balance Report File"), validators=[pdf_file_validator], upload_to=get_non_tax_file_upload_path, blank=True, null=True)

    profit_loss_file = models.FileField(verbose_name=_(
        "Profit Loss File"), validators=[pdf_file_validator], upload_to=get_non_tax_file_upload_path, blank=True, null=True)

    sold_product_file = models.FileField(verbose_name=_(
        "Sold Product File"), validators=[pdf_file_validator], upload_to=get_non_tax_file_upload_path, blank=True, null=True)

    account_turnover_file = models.FileField(verbose_name=_(
        "Account Turn Over File"), validators=[pdf_file_validator], upload_to=get_non_tax_file_upload_path, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.company.company_title} › {self.year}"

    class Meta:
        verbose_name = _("Balance Report")
        verbose_name_plural = _("Balance Reports")
        unique_together = [['company', 'month', 'year'],]


class BaseRequest(models.Model):
    
    REQUEST_STATUS_NEW = 'new'
    REQUEST_STATUS_PENDING = 'pending'
    REQUEST_STATUS_ACCEPTED = 'accepted'
    REQUEST_STATUS_REJECTED = 'rejected'

    REQUEST_STATUS_CHOICES = [
        (REQUEST_STATUS_NEW, _("New")),
        (REQUEST_STATUS_PENDING, _("Pending")),
        (REQUEST_STATUS_ACCEPTED, _("Accepted")),
        (REQUEST_STATUS_REJECTED, _("Rejected")),
    ]

    company = models.ForeignKey(
        CompanyProfile, on_delete=models.CASCADE, verbose_name=_("Company"), null=True)

    subject = models.TextField(
        blank=True, null=True, verbose_name=_("Subject"))

    status = models.CharField(verbose_name=_(
        "Status"), max_length=10, choices=REQUEST_STATUS_CHOICES, default=REQUEST_STATUS_NEW)

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Created At"))

    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Updated At"))

    service = models.ForeignKey(CompanyService, related_name="services",
                                on_delete=models.SET_NULL, verbose_name=_("Service"), null=True)

    class Meta:
        abstract = True
        verbose_name = _("BaseRequest")
        verbose_name_plural = _("BaseRequests")


class DiagnosticRequest(BaseRequest):

    tax_record = models.ForeignKey(TaxDeclaration, on_delete=models.CASCADE, verbose_name=_(
        "Tax Record"), null=True, blank=True)

    balance_record = models.ForeignKey(BalanceReport, on_delete=models.CASCADE, verbose_name=_(
        "Balance Record"), null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.company.company_title} › {self.status}"

    class Meta:
        verbose_name = _("Diagnostic Request")
        verbose_name_plural = _("Diagnostic Requests")
