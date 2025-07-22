from django.utils.translation import gettext_lazy as _
from django.db import models


from constants.validators import Validator as _validator


class DomesticSale(models.Model):
    class SaleMethod(models.TextChoices):
        ONLINE = "online", _("Online")
        OFFLINE = "offline", _("Offline")

    class PaymentMethod(models.TextChoices):
        CASH = "cash", _("Cash")
        INSTALLEMENT = "installment", _("Installment")

    company = models.ForeignKey(
        "company.CompanyProfile",
        on_delete=models.CASCADE,
        related_name="domestic_sales",
        verbose_name=_("Company"),
    )
    customer_name = models.CharField(
        max_length=255,
        verbose_name=_("Customer Name"),
    )
    product_code = models.CharField(
        max_length=10,
        verbose_name=_("Product Code"),
    )
    sold_amount = models.PositiveSmallIntegerField(
        verbose_name=_("Sold Amount"),
        validators=[_validator.min_numeric_value_validator()],
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Unit Price"),
    )
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Discount Price"),
    )
    sale_method = models.CharField(
        max_length=7,
        choices=SaleMethod.choices,
        default=SaleMethod.ONLINE,
        verbose_name=_("Sale Method"),
    )
    payment_method = models.CharField(
        max_length=11,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CASH,
        verbose_name=_("Payment Method"),
    )
    sold_at = models.DateField(verbose_name=_("Sold At"))
    updated_at = models.DateField(auto_now_add=True, verbose_name=_("Updated At"))

    def __str__(self):
        return f"{self.company.title} Domestic Sale: {self.sold_at}"

    class Meta:
        verbose_name = _("Domestic Sale")
        verbose_name_plural = _("Domestic Sales")
        constraints = [
            models.UniqueConstraint(
                name="unique_company_sale_date",
                fields=[
                    "company",
                    "sold_at",
                ],
            )
        ]


class ForeignSale(models.Model):
    class SaleMethod(models.TextChoices):
        ONLINE = "online", _("Online")
        EXHIBITION = "exhibition", _("Exhibition")

    class PaymentStatus(models.TextChoices):
        ADVANCE_PAYMENT = "ap", _("Advance Payment")
        OPEN_ACCOUNT = "oa", _("Open Account")
        RECEIVABLE = "re", _("Receivable")
        DOCUMENT = "do", _("Document")

    class TransferCondition(models.TextChoices):
        LAND = "land", _("Land")
        RAIL = "rail", _("Rail")
        SEA = "sea", _("Sea")
        AIR = "air", _("Air")

    company = models.ForeignKey(
        "company.CompanyProfile",
        on_delete=models.CASCADE,
        related_name="foreign_sales",
        verbose_name=_("Company"),
    )
    customer_name = models.CharField(
        max_length=255,
        verbose_name=_("Customer Name"),
    )
    product_code = models.CharField(
        max_length=10,
        verbose_name=_("Product Code"),
    )
    sold_amount = models.PositiveSmallIntegerField(
        verbose_name=_("Sold Amount"),
        validators=[_validator.min_numeric_value_validator()],
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Unit Price"),
    )
    contract_date = models.DateField(verbose_name=_("Contract Date"))
    delivery_date = models.DateField(verbose_name=_("Delivery Date"))
    target_country = models.CharField(max_length=50, verbose_name=_("Target Country"))
    area = models.CharField(max_length=50, verbose_name=_("Area"))
    customer_approval = models.BooleanField(
        verbose_name=_("Customer Approval"), default=True
    )
    sale_method = models.CharField(
        max_length=10,
        choices=SaleMethod.choices,
        default=SaleMethod.ONLINE,
        verbose_name=_("Sale Method"),
    )
    payment_status = models.CharField(
        max_length=10,
        choices=PaymentStatus.choices,
        default=PaymentStatus.ADVANCE_PAYMENT,
        verbose_name=_("Payment Status"),
    )
    transfer_condition = models.CharField(
        max_length=10,
        choices=TransferCondition.choices,
        default=TransferCondition.AIR,
        verbose_name=_("Transfer Condition"),
    )
    trading_currency = models.CharField(
        max_length=10,
        verbose_name=_("Trading Currency"),
    )
    exchange_rate = models.CharField(
        max_length=10,
        verbose_name=_("Exchange Rate"),
    )
    sale_amount = models.CharField(
        max_length=10,
        verbose_name=_("Sale Amount"),
    )

    def __str__(self):
        return f"{self.company.title} Foreign Sale: {self.contract_date}"

    class Meta:
        verbose_name = _("Foreign Sale")
        verbose_name_plural = _("Foreign Sales")
