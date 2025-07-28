from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeStampedModel
from apps.core.utils import GeneralUtils
from constants.validators import Validator as _validator


class DomesticSaleData(TimeStampedModel):
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


class ForeignSaleData(TimeStampedModel):
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


def get_customer_data_file_upload_path(instance, filename):
    path = GeneralUtils(path="sales_customer_files", fields=["company"]).rename_folder(
        instance, filename
    )
    return path


class CustomerSaleFile(TimeStampedModel):
    company = models.ForeignKey(
        "company.CompanyProfile",
        related_name="customer_data_files",
        verbose_name=_("Company"),
        on_delete=models.CASCADE,
    )
    file = models.FileField(
        verbose_name=_("File"),
        upload_to=get_customer_data_file_upload_path,
        validators=[_validator.excel_file_validator],
    )

    def __str__(self):
        return self.company.title

    class Meta:
        verbose_name = _("Customer Sale File")
        verbose_name_plural = _("Customer Sale Files")


class CustomerSaleData(TimeStampedModel):
    class SaleArea(models.TextChoices):
        DOMESTIC = "d", _("Domestic")
        FOREIGN = "f", _("Foreign")

    class CustomerChannel(models.TextChoices):
        SOCIAL = "so", _("Social")
        ONLINE = "on", _("Online")
        SEO = "se", _("Seo")
        EMAIL = "em", _("Email")
        PHONE = "ph", _("Phone")
        EXHIBITION = "ex", _("Exhibition")
        PEOPLE = "pe", _("People")
        OTHER = "ot", _("Other")

    company = models.ForeignKey(
        "company.CompanyProfile",
        related_name="customer_data",
        verbose_name=_("Company"),
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=50,
        verbose_name=_("Name(Person/Company)"),
    )
    sale_area = models.CharField(
        verbose_name=_("Sale Area"),
        choices=SaleArea.choices,
        max_length=1,
    )
    channel = models.CharField(
        max_length=20,
        choices=CustomerChannel.choices,
    )
    city = models.ForeignKey(
        "core.City",
        verbose_name=_("City"),
        on_delete=models.DO_NOTHING,
    )
    area = models.CharField(
        max_length=50,
        verbose_name=_("Area"),
    )
    first_purchase_date = models.DateField(
        verbose_name=_("First Purchase Date"),
    )
    last_purchase_date = models.DateField(
        verbose_name=_("Last Purchase Date"),
    )
    description = models.TextField(
        verbose_name=_("Description"),
    )

    def __str__(self):
        return f"{self.company.title}: {self.description}"

    class Meta:
        verbose_name = _("Customer Sale Data")
        verbose_name_plural = _("Customers Sale Data")
        constraints = [
            models.UniqueConstraint(
                name="unique_company_customer",
                fields=[
                    "company",
                    "name",
                ],
            )
        ]


def get_product_data_file_upload_path(instance, filename):
    path = GeneralUtils(path="sales_customer_files", fields=["company"]).rename_folder(
        instance, filename
    )
    return path


class ProductDataFile(TimeStampedModel):
    company = models.ForeignKey(
        "company.CompanyProfile",
        related_name="product_data_files",
        verbose_name=_("Company"),
        on_delete=models.CASCADE,
    )
    file = models.FileField(
        verbose_name=_("File"),
        upload_to=get_product_data_file_upload_path,
        validators=[_validator.excel_file_validator],
    )

    class Meta:
        verbose_name = _("Product Date File")
        verbose_name_plural = _("Product Date Files")


class ProductData(TimeStampedModel):
    class ProductUnit(models.TextChoices):
        METRE = "me", _("Metre")
        SQUAR_METRE = "sm", _("Square Metre")
        GRAM = "g", _("Gram")
        KILOGRAM = "kg", _("Kilo Gram")
        TON = "t", _("Ton")
        NUMBER = "n", _("Number")
        CUBIC_CENTIMETRE = "cc", _("CC")
        LITRE = "l", _("Litre")
        HOUR = "h", _("Hour")
        MINUTW = "mi", _("Minute")
        OTHER = "o", _("Other")

    company = models.ForeignKey(
        "company.CompanyProfile",
        related_name="products",
        verbose_name=_("Company"),
        on_delete=models.CASCADE,
    )
    code = models.CharField(
        max_length=50,
        verbose_name=_("Product/Service Code"),
    )
    name = models.CharField(
        max_length=50,
        verbose_name=_("Name"),
    )
    unit = models.CharField(
        max_length=50,
        choices=ProductUnit.choices,
        verbose_name=_("Unit"),
    )
    description = models.TextField(verbose_name=_("Description"))

    class Meta:
        verbose_name = _("Product/Service Data")
        verbose_name_plural = _("Products/Services Data")
        constraints = [
            models.UniqueConstraint(
                name="unique_company_product",
                fields=[
                    "company",
                    "code",
                ],
            )
        ]
