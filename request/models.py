from django.utils.translation import gettext_lazy as _
from django.db import models


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
        "company.CompanyProfile", on_delete=models.CASCADE, verbose_name=_("Company"), null=True)

    subject = models.TextField(
        blank=True, null=True, verbose_name=_("Subject"))

    status = models.CharField(
        verbose_name=_("Status"), max_length=10, choices=REQUEST_STATUS_CHOICES, default=REQUEST_STATUS_NEW)

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Created At"))

    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Updated At"))

    # Define the service field without a related_name here since it's abstract
    service = models.ForeignKey(
        "company.CompanyService", 
        on_delete=models.SET_NULL, 
        verbose_name=_("Service"), 
        null=True
    )

    class Meta:
        abstract = True
        verbose_name = _("BaseRequest")
        verbose_name_plural = _("BaseRequests")


class FinanceRequest(BaseRequest):
    # Override the service field with a unique related_name
    service = models.ForeignKey(
        "company.CompanyService", 
        related_name="finance_requests",  # Unique related_name
        on_delete=models.SET_NULL, 
        verbose_name=_("Service"), 
        null=True
    )

    tax_record = models.ForeignKey(
        "finance.TaxDeclarationFile", 
        on_delete=models.CASCADE, 
        verbose_name=_("Tax Record"), 
        null=True, 
        blank=True, 
        related_name="finance_request_tax_record"
    )

    balance_record = models.ForeignKey(
        "finance.BalanceReportFile", 
        on_delete=models.CASCADE, 
        verbose_name=_("Balance Record"), 
        null=True, 
        blank=True, 
        related_name="finance_request_balance_record"
    )

    def __str__(self) -> str:
        return f"{self.company.company_title} › {self.status}"

    class Meta:
        verbose_name = _("Finance Request")
        verbose_name_plural = _("Finance Requests")


class ManagementRequest(BaseRequest):
    # Override the service field with a unique related_name
    service = models.ForeignKey(
        "company.CompanyService", 
        related_name="management_requests",  # Unique related_name
        on_delete=models.SET_NULL, 
        verbose_name=_("Service"), 
        null=True
    )

    human_resource_record = models.ForeignKey(
        "management.HumanResource", 
        verbose_name=_("Human Resource Record"), 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name="management_request_human_resource_record"
    )

    def __str__(self):
        return f"{self.company.company_title} › {self.status}"

    class Meta:
        verbose_name = _("Management Request")
        verbose_name_plural = _("Management Requests")
