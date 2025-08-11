from django.db import models
from django.utils.translation import gettext_lazy as _
from django_lifecycle.decorators import hook
from django_lifecycle.hooks import AFTER_CREATE
from django_lifecycle.models import LifecycleModelMixin

from apps.core.models import TimeStampedModel
from apps.salesdata.services import SaleDataService as _service
from apps.salesdata.services.excel_reader_service import Reader as _reader
from constants.validators import Validator as _validator


class DomesticSaleFile(LifecycleModelMixin, TimeStampedModel):
    company = models.ForeignKey(
        "company.CompanyProfile",
        on_delete=models.CASCADE,
        related_name="domestic_sale_files",
        verbose_name=_("Company"),
    )
    file = models.FileField(
        validators=[_validator.excel_file_validator],
        upload_to=_service.set_domestic_data_file_upload_path,
        verbose_name=_("File"),
    )

    def __str__(self):
        return self.company.title

    @hook(AFTER_CREATE)
    def read_file(self):
        _reader.process_domestic_file(self.pk)

    class Meta:
        verbose_name = _("Domestic Sale File")
        verbose_name_plural = _("Domestic Sale Files")


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
    factor_number = models.PositiveSmallIntegerField(verbose_name=_("Factor Number"))
    customer_name = models.CharField(
        max_length=255,
        verbose_name=_("Customer Name"),
    )
    product_code = models.PositiveSmallIntegerField(
        verbose_name=_("Product Code"),
    )
    product_name = models.CharField(verbose_name=_("Product Name"), max_length=50)
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

    def __str__(self):
        return f"{self.company.title} Domestic Sale: {self.sold_at}"

    class Meta:
        verbose_name = _("Domestic Sale")
        verbose_name_plural = _("Domestic Sales")


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
    product_code = models.ForeignKey(
        "ProductData",
        on_delete=models.CASCADE,
        related_name="foreign_sale",
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


class CustomerSaleFile(LifecycleModelMixin, TimeStampedModel):
    company = models.ForeignKey(
        "company.CompanyProfile",
        related_name="customer_data_files",
        verbose_name=_("Company"),
        on_delete=models.CASCADE,
    )
    file = models.FileField(
        verbose_name=_("File"),
        upload_to=_service.set_customer_data_file_upload_path,
        validators=[_validator.excel_file_validator],
    )

    def __str__(self):
        return self.company.title

    @hook(AFTER_CREATE)
    def read_file(self):
        _reader.process_customer_list_file(self.pk)

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
    city = models.CharField(
        max_length=20,
        verbose_name=_("City"),
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


class ProductDataFile(LifecycleModelMixin,TimeStampedModel):
    company = models.ForeignKey(
        "company.CompanyProfile",
        related_name="product_data_files",
        verbose_name=_("Company"),
        on_delete=models.CASCADE,
    )
    file = models.FileField(
        verbose_name=_("File"),
        upload_to=_service.set_product_data_file_upload_path,
        validators=[_validator.excel_file_validator],
    )

    @hook(AFTER_CREATE)
    def read_file(self):
        _reader.process_product_data_file(self.pk)
    class Meta:
        verbose_name = _("Product/Service Data File")
        verbose_name_plural = _("Products/Services Data Files")


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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Product/Service Data")
        verbose_name_plural = _("Products/Services Data")
        # constraints = [
        #     models.UniqueConstraint(
        #         name="unique_company_product",
        #         fields=[
        #             "company",
        #             "code",
        #         ],
        #     )
        # ]


class ProductLog(TimeStampedModel):
    company = models.ForeignKey(
        "company.CompanyProfile",
        related_name="products_log",
        verbose_name=_("Company"),
        on_delete=models.CASCADE,
    )
    product_name = models.CharField(
        max_length=120,
        verbose_name=_("Product"),
    )
    production_date = models.DateField(
        verbose_name=_("Production Date"), help_text=_("The date of production.")
    )
    total_produced = models.PositiveIntegerField(
        verbose_name=_("Total Production Count"),
        help_text=_("Total number of units produced on this date."),
    )
    total_returned = models.PositiveIntegerField(
        verbose_name=_("Returned Products Count"),
        default=0,
        help_text=_("Number of units returned from customers."),
    )
    total_rejected = models.PositiveIntegerField(
        verbose_name=_("Rejected Products Count"),
        default=0,
        help_text=_("Number of units that failed quality control."),
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Unit Price"),
    )

    @property
    def net_quantity(self):
        return self.total_produced - self.total_returned - self.total_rejected

    @property
    def total_value(self):
        return self.net_quantity * self.unit_price

    def __str__(self):
        return f"{self.product_name} on {self.production_date}"

    class Meta:
        verbose_name = _("Product Log")
        verbose_name_plural = _("Product Logs")


class ProductLogFile(LifecycleModelMixin, TimeStampedModel):
    company = models.ForeignKey(
        "company.CompanyProfile",
        related_name="product_log_files",
        verbose_name=_("Company"),
        on_delete=models.CASCADE,
    )
    file = models.FileField(
        verbose_name=_("File"),
        upload_to=_service.set_product_logs_file_upload_path,
        validators=[_validator.excel_file_validator],
    )

    @hook(AFTER_CREATE)
    def read_file(self):
        _reader.process_product_log_file(self.pk)

    def __str__(self):
        return self.company.title

    class Meta:
        verbose_name = _("Product Log File")
        verbose_name_plural = _("Product Logs Files")
