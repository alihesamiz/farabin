from django.utils.translation import gettext_lazy as _
from django.db import models
# Create your models here.



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

    status = models.CharField(verbose_name=_(
        "Status"), max_length=10, choices=REQUEST_STATUS_CHOICES, default=REQUEST_STATUS_NEW)

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Created At"))

    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Updated At"))

    service = models.ForeignKey("company.CompanyService", related_name="services",
                                on_delete=models.SET_NULL, verbose_name=_("Service"), null=True)

    class Meta:
        abstract = True
        verbose_name = _("BaseRequest")
        verbose_name_plural = _("BaseRequests")


class FinanceRequest(BaseRequest):

    tax_record = models.ForeignKey("finance.TaxDeclarationFile", on_delete=models.CASCADE, verbose_name=_(
        "Tax Record"), null=True, blank=True)

    balance_record = models.ForeignKey("finance.BalanceReportFile", on_delete=models.CASCADE, verbose_name=_(
        "Balance Record"), null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.company.company_title} › {self.status}"

    class Meta:
        verbose_name = _("Finance Request")
        verbose_name_plural = _("Finance Requests")