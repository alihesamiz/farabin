from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractBaseUser as BaseUser

from diagnostics.utils import CustomUtils
from .validators import phone_number_validator
from .managers import UserManager
from datetime import timedelta
import random
from uuid import uuid4

# Create your models here.


####################################
"""User Model"""


class User(BaseUser):

    phone_number = models.CharField(
        max_length=11, unique=True, validators=[phone_number_validator])
    national_code = models.CharField(max_length=11, unique=True)
    otp = models.CharField(max_length=6)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'national_code'
    REQUIRED_FIELDS = ['phone_number']

    objects = UserManager()

    def __str__(self) -> str:
        return f"{self.phone_number}"

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    @property
    def is_admin(self):
        return self.is_superuser


####################################
"""OTP Model"""


class OTP(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='+')
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        # OTP is valid for 10 minutes
        return self.created_at >= timezone.now() - timedelta(minutes=3)

    def generate_otp(self):
        return random.randint(100000, 999999)


####################################
"""Company Model"""


class CompanyProfile(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4)

    NEWBIE_LICENSE = 'newbie'
    INNOVATIVE_LICENSE = 'innovative'
    TECHNOLOGICAL_LICENSE = 'technological'
    LICENSE_CHOICES = [
        (NEWBIE_LICENSE, _("Newbie")),
        (INNOVATIVE_LICENSE, _("Innovative")),
        (TECHNOLOGICAL_LICENSE, _("Technological")),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name=_("User"))

    company_title = models.CharField(
        max_length=255, verbose_name=_("Company Title"))

    email = models.EmailField(
        max_length=255, unique=True, verbose_name=_("Email"))

    social_code = models.CharField(
        max_length=10, unique=True, verbose_name=_("Social Code"))

    manager_name = models.CharField(
        max_length=255, verbose_name=_("Manager Full Name"))

    license = models.CharField(
        max_length=15, choices=LICENSE_CHOICES, verbose_name=_("License Type"))

    work_place = models.ForeignKey(
        'Institute', on_delete=models.CASCADE, verbose_name=_("Work Place"))

    tech_field = models.CharField(
        max_length=500, null=True, blank=True, verbose_name=_("Technical Field"))

    insurance_list = models.SmallIntegerField(
        default=1, verbose_name=_("Insurance List"))

    organization = models.ForeignKey(
        'Organization', null=True, blank=True, verbose_name=_("Organization"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Company Profile")
        verbose_name_plural = _("Company Profiles")

    def __str__(self) -> str:
        return f"{self.company_title}- {self.user.national_code}"


####################################
"""Organizations Model"""


class Organization(models.Model):
    DEFEND = 'defend'

    ORGANIZATION_CHOICES = [
        (DEFEND, _("Defend"))
    ]
    organization_title = models.CharField(
        choices=ORGANIZATION_CHOICES, default=DEFEND, max_length=50, blank=True, null=True, verbose_name=_("Organization Title")
    )
    custom_organization_title = models.CharField(
        max_length=50, blank=True, null=True,
        help_text=_(
            "Enter a custom organization title if none of the choices apply."), verbose_name=_("Other Organization Title")
    )

    class Meta:
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")

    def __str__(self) -> str:
        return f"{self.custom_organization_title}" if self.custom_organization_title else f"{self.get_organization_title_display()}"


####################################
"""City and province Models"""


class City(models.Model):

    name = models.CharField(max_length=200, verbose_name=_('Name'))

    province = models.ForeignKey(
        'Province', related_name='cities', on_delete=models.CASCADE, default="", verbose_name=_('Province'))

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")


class Province(models.Model):

    name = models.CharField(max_length=200, unique=True,
                            verbose_name=_('Name'))

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Province")
        verbose_name_plural = _("Provinces")


####################################
"""Work place Model"""


class Institute(models.Model):

    title = models.CharField(max_length=250, verbose_name=_('Title'))

    province = models.ForeignKey(
        Province, on_delete=models.CASCADE, verbose_name=_('Province'))

    def __str__(self) -> str:
        return f"{self.title} , {self.province}"

    class Meta:
        verbose_name = _("Institute")
        verbose_name_plural = _("Institutes")


####################################
"""diagnostic Models"""


class SoldProductFee(models.Model):
    financial_asset = models.ForeignKey(
        'FinancialAsset', on_delete=models.CASCADE, related_name='sold_product_fees', verbose_name=_('Financial Asset'))
    consuming_material = models.DecimalField(default=0,
                                             max_digits=20, decimal_places=0, verbose_name=_('Consuming Material'))
    production_fee = models.DecimalField(default=0,
                                         max_digits=20, decimal_places=0, verbose_name=_('Production Fee'))
    construction_overhead = models.DecimalField(default=0,
                                                max_digits=20, decimal_places=0, verbose_name=_('Construction Overhead'))
    production_total_price = models.DecimalField(
        max_digits=20, decimal_places=0, default=0, verbose_name=_('Production Total Price'))
    current_constructing_product_first_period_inventory = models.DecimalField(
        max_digits=20, decimal_places=0, default=0, verbose_name=_('Current Constructing Product First Period'))
    current_constructing_product_end_period_inventory = models.DecimalField(
        max_digits=20, decimal_places=0, default=0, verbose_name=_('Current Constructing Product End Period'))
    produced_product_total_price = models.DecimalField(
        max_digits=20, decimal_places=0, default=0, verbose_name=_('Produced Product Total Price'))
    first_period_produced_inventory = models.DecimalField(
        max_digits=20, decimal_places=0, default=0, verbose_name=_('First Period Produced Inventory'))
    period_bought_product = models.DecimalField(
        max_digits=20, decimal_places=0, default=0, verbose_name=_('Period Bought Product'))
    ready_for_sale_product = models.DecimalField(
        max_digits=20, decimal_places=0, default=0, verbose_name=_('Ready for Sale Product'))
    end_period_inventory = models.DecimalField(
        max_digits=20, decimal_places=0, default=0, verbose_name=_('End Period Inventory'))
    product_other = models.DecimalField(
        max_digits=20, decimal_places=0, default=0, verbose_name=_('Other Product'))
    sold_product_total_price = models.DecimalField(default=0,
                                                   max_digits=20, decimal_places=0, verbose_name=_('Sold Product Total Price'))

    class Meta:
        unique_together = ('financial_asset',)
        verbose_name = _("Sold Product Fee")
        verbose_name_plural = _("Sold Products Fee")


class ProfitLossStatement(models.Model):
    financial_asset = models.ForeignKey(
        'FinancialAsset', on_delete=models.CASCADE, related_name='profit_loss_statements', verbose_name=_('Financial Asset'))
    operational_income = models.DecimalField(default=0,
                                             max_digits=20, decimal_places=0, verbose_name=_('Operational Income'))
    operational_income_expense = models.DecimalField(default=0,
                                                     max_digits=20, decimal_places=0, verbose_name=_('Operational Income Expense'))
    gross_profit = models.DecimalField(default=0,
                                       max_digits=20, decimal_places=0, verbose_name=_('Gross Profit'))
    salary_fee = models.DecimalField(default=0,
                                     max_digits=20, decimal_places=0, verbose_name=_('Salary Fee'))
    marketing_fee = models.DecimalField(default=0,
                                        max_digits=20, decimal_places=0, verbose_name=_('Marketing Fee'))
    doubtful_burnt_claims_fee = models.DecimalField(
        max_digits=20, default=0, decimal_places=0, verbose_name=_('Doubtful Burnt Claims Fee'))
    attendance_fee = models.DecimalField(default=0,
                                         max_digits=20, decimal_places=0, verbose_name=_('Attendance Fee'))
    accounting_fee = models.DecimalField(default=0,
                                         max_digits=20, decimal_places=0, verbose_name=_('Accounting Fee'))
    consulting_fee = models.DecimalField(default=0,
                                         max_digits=20, decimal_places=0, verbose_name=_('Consulting Fee'))
    rental_fee = models.DecimalField(default=0,
                                     max_digits=20, decimal_places=0, verbose_name=_('Rental Fee'))
    other_general_expense = models.DecimalField(default=0,
                                                max_digits=20, decimal_places=0, verbose_name=_('Other General Expense'))
    total_general_expense = models.DecimalField(default=0,
                                                max_digits=20, decimal_places=0, verbose_name=_('Total General Expense'))
    other_operation_income = models.DecimalField(default=0,
                                                 max_digits=20, decimal_places=0, verbose_name=_('Other Operational Income'))
    other_operational_expense = models.DecimalField(default=0,
                                                    max_digits=20, decimal_places=0, verbose_name=_('Other Operational Expense'))
    operational_profit = models.DecimalField(default=0,
                                             max_digits=20, decimal_places=0, verbose_name=_('Operational Profit'))
    immovable_property_sale_profit = models.DecimalField(default=0,
                                                         max_digits=20, decimal_places=0, verbose_name=_('Immovable Property Sale Profit'))
    other_assets_sale_profit = models.DecimalField(default=0,
                                                   max_digits=20, decimal_places=0, verbose_name=_('Other Assets Sale Profit'))
    material_sale_profit = models.DecimalField(default=0,
                                               max_digits=20, decimal_places=0, verbose_name=_('Material Sale Profit'))
    investment_sale_profit = models.DecimalField(default=0,
                                                 max_digits=20, decimal_places=0, verbose_name=_('Investment Sale Profit'))
    interpretation_profit = models.DecimalField(default=0,
                                                max_digits=20, decimal_places=0, verbose_name=_('Interpretation Profit'))
    dividend_profit = models.DecimalField(default=0,
                                          max_digits=20, decimal_places=0, verbose_name=_('Dividend Profit'))
    investment_profit = models.DecimalField(default=0,
                                            max_digits=20, decimal_places=0, verbose_name=_('Investment Profit'))
    bank_deposit_profit = models.DecimalField(default=0,
                                              max_digits=20, decimal_places=0, verbose_name=_('Bank Deposit Profit'))
    rental_income = models.DecimalField(default=0,
                                        max_digits=20, decimal_places=0, verbose_name=_('Rental Income'))
    incidental_income = models.DecimalField(default=0,
                                            max_digits=20, decimal_places=0, verbose_name=_('Incidental Income'))
    other_non_operationl_income_expense = models.DecimalField(default=0,
                                                              max_digits=20, decimal_places=0, verbose_name=_('Other Non-Operational Income/Expense'))
    net_value_other_non_operationl_income_expense = models.DecimalField(default=0,
                                                                        max_digits=20, decimal_places=0, verbose_name=_('Net Value Other Non-Operational Income/Expense'))
    financial_expense = models.DecimalField(default=0,
                                            max_digits=20, decimal_places=0, verbose_name=_('Financial Expense'))
    proceed_profit = models.DecimalField(default=0,
                                         max_digits=20, decimal_places=0, verbose_name=_('Proceed Profit'))
    current_year_income_tax = models.DecimalField(default=0,
                                                  max_digits=20, decimal_places=0, verbose_name=_('Current Year Income Tax'))
    prev_year_income_tax = models.DecimalField(default=0,
                                               max_digits=20, decimal_places=0, verbose_name=_('Previous Year Income Tax'))
    profit_after_tax = models.DecimalField(default=0,
                                           max_digits=20, decimal_places=0, verbose_name=_('Profit After Tax'))

    class Meta:
        unique_together = ('financial_asset',)
        verbose_name = _("Profit And Loss Statement")
        verbose_name_plural = _("Profit And Loss Statements")


class BalanceReport(models.Model):

    RENAME_REPORT_PATH = CustomUtils(
        path="financial_analysis/diagnoses/files",
        fields=['financial_asset__company__title']
    )

    financial_asset = models.ForeignKey(
        'FinancialAsset', on_delete=models.CASCADE, related_name='balance_reports', verbose_name=_('Financial Asset'))

    balance_report_file = models.FileField(verbose_name=_(
        'Balance Report File'), upload_to=RENAME_REPORT_PATH.rename_folder, blank=True, null=True)
    # current assets

    advance_payment = models.DecimalField(default=0,
                                          max_digits=20, decimal_places=0, verbose_name=_('Advance Payment'))
    inventory = models.DecimalField(default=0,
                                    max_digits=20, decimal_places=0, verbose_name=_('Inventory'))
    trade_receivable = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('Recievable Trade Account'))
    short_term_investment = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('Short term Investment'))

    cash_balance = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('Cash Balance'))

    held_non_current_asset = models.DecimalField(default=0,
                                                 max_digits=20, decimal_places=0, verbose_name=_('Non-current assets held for sale'))
    current_shareholder_asset = models.DecimalField(default=0,
                                                    max_digits=20, decimal_places=0, verbose_name=_('Current Partner/Shareholder'))
    total_current_asset = models.DecimalField(default=0,
                                              max_digits=20, decimal_places=0, verbose_name=_('Total Current Asset'))

    # non-current assets

    tangible_fixed_asset = models.DecimalField(default=0,
                                               max_digits=20, decimal_places=0, verbose_name=_('Tangible Fixed Asset'))
    property_investment = models.DecimalField(default=0,
                                              max_digits=20, decimal_places=0, verbose_name=_('Property Investment'))
    intangible_asset = models.DecimalField(default=0,
                                           max_digits=20, decimal_places=0, verbose_name=_('Intangible Asset'))
    long_term_investment = models.DecimalField(default=0,
                                               max_digits=20, decimal_places=0, verbose_name=_('Long Term Investment'))
    long_term_receivable = models.DecimalField(default=0,
                                               max_digits=20, decimal_places=0, verbose_name=_('Long Term Receivable'))
    other_asset = models.DecimalField(default=0,
                                      max_digits=20, decimal_places=0, verbose_name=_('Other Asset'))
    total_non_current_asset = models.DecimalField(default=0,
                                                  max_digits=20, decimal_places=0, verbose_name=_('Total Non-Current Asset'))

    # ownership right
    capital = models.DecimalField(default=0,
                                  max_digits=20, decimal_places=0, verbose_name=_("Wealth"))
    capital_increase = models.DecimalField(default=0,
                                           max_digits=20, decimal_places=0, verbose_name=_("Wealth Increase"))
    share_spend = models.DecimalField(default=0,
                                      max_digits=20, decimal_places=0, verbose_name=_("Share Spend"))
    treasury_share_spend = models.DecimalField(default=0,
                                               max_digits=20, decimal_places=0, verbose_name=_("Treasury Share Spend"))
    legal_reserve = models.DecimalField(default=0,
                                        max_digits=20, decimal_places=0, verbose_name=_("Legal Reserve"))
    other_reserve = models.DecimalField(default=0,
                                        max_digits=20, decimal_places=0, verbose_name=_("Other Reserve"))
    revaluation_surplus = models.DecimalField(default=0, max_digits=20, decimal_places=0, verbose_name=_(
        "Asset Revaluation Surplus and Other Unrealized Gains"))
    accumulated_profit_loss = models.DecimalField(default=0,
                                                  max_digits=20, decimal_places=0, verbose_name=_("Accumulated Profit and Loss"))
    treasury_share = models.DecimalField(default=0,
                                         max_digits=20, decimal_places=0, verbose_name=_("Treasury Share"))

    ownership_right_total = models.DecimalField(default=0,
                                                max_digits=20, decimal_places=0, verbose_name=_("Ownership right total"))

    # Current Debt
    trade_payable = models.DecimalField(default=0,
                                        max_digits=20, decimal_places=0, verbose_name=_("Trade Payable"))
    paid_tax = models.DecimalField(default=0,
                                   max_digits=20, decimal_places=0, verbose_name=_("Paid Tax"))
    dividend_payable = models.DecimalField(default=0,
                                           max_digits=20, decimal_places=0, verbose_name=_("Dividend Payable"))
    financial_facility = models.DecimalField(default=0,
                                             max_digits=20, decimal_places=0, verbose_name=_("Financial Facility"))
    reserves = models.DecimalField(default=0,
                                   max_digits=20, decimal_places=0, verbose_name=_("Reserves"))
    advance = models.DecimalField(default=0,
                                  max_digits=20, decimal_places=0, verbose_name=_("Advance"))
    held_for_sale_liability = models.DecimalField(default=0, max_digits=20, decimal_places=0, verbose_name=_(
        "Liability related to non-current asset held for sale"))
    current_shareholder_debt = models.DecimalField(default=0,
                                                   max_digits=20, decimal_places=0, verbose_name=_("Current Partner/Shareholder"))
    total_current_debt = models.DecimalField(default=0,
                                             max_digits=20, decimal_places=0, verbose_name=_('Total Current Debt'))

    # Non Current Debt
    long_term_payable = models.DecimalField(default=0,
                                            max_digits=20, decimal_places=0, verbose_name=_("Longterm Payable"))
    long_term_financial = models.DecimalField(default=0,
                                              max_digits=20, decimal_places=0, verbose_name=_("Longterm Financial Facilities"))
    employee_termination_benefit_reserve = models.DecimalField(default=0,
                                                               max_digits=20, decimal_places=0, verbose_name=_("Reserve Employee Termination Benefit"))
    total_non_current_debt = models.DecimalField(default=0,
                                                 max_digits=20, decimal_places=0, verbose_name=_('Total Non-Current Debt'))

    net_sale = models.DecimalField(default=0,
                                   max_digits=20, decimal_places=0, verbose_name=_('Net Sale'))
    net_profit = models.DecimalField(default=0,
                                     max_digits=20, decimal_places=0, verbose_name=_('Net Profit'))

    class Meta:
        unique_together = ('financial_asset',)
        verbose_name = _("Balance Report")
        verbose_name_plural = _("Balance Reports")


class AccountTurnOver(models.Model):
    financial_asset = models.ForeignKey(
        'FinancialAsset', on_delete=models.CASCADE, related_name='account_turnovers', verbose_name=_('Financial Asset'))
    profit_after_tax = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('Profit After Tax'))
    first_year_accumulated_profit = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('First Year  Accumulated Profit'))
    correcting_mistake = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('Correcting Mistake'))
    accounting_method_change = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('Accounting Method Change'))
    first_year_accumulated_profit_balanced = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('First Year`s Accumulated Profit Balanced'))
    transfer_from_reserve = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('Transfer From Reserve'))
    other_account_turnover = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('Other Account Turnover'))
    allocable_profit = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('Allocable Profit'))
    share_profit = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('Share Profit'))
    legal_reserve = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('Legal Reserve'))
    wealth_increase = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('Wealth Increase'))
    current_wealt_increase = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('Current Wealt Increase'))
    other_reserves = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('Other Reserves'))
    treasury_share_purchase = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('Treasury Share Purchase'))
    treasury_share_sale = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('Treasury Share Sale'))
    treasury_share_sale_profit = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('Treasury Share Sale Profit'))
    board_reward = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('Board Reward'))
    other_profit = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('Other Profit'))
    total_allocated_profit = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('Total Allocated Profit'))
    end_year_accumulated_profit = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('End Year`s Accumulated profit'))

    class Meta:
        unique_together = ('financial_asset',)
        verbose_name = _("Account TurnOver")
        verbose_name_plural = _("Accounts Turnovers")


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

    other_capital_providing = models.CharField(
        max_length=20, verbose_name=_("Capital Providing Other"), null=True, blank=True)

    class Meta:
        verbose_name = _('Life Cycle')
        verbose_name_plural = _('Life Cycles')

    def __str__(self):
        return self.get_capital_providing_display()


RENAME_TAX_DECLARATION_PATH = CustomUtils(
    path="financial_analysis/diagnoses/files", 
    fields=['financial_asset__company__company_title', 'financial_asset__year']
)


class TaxDeclarationFile(models.Model):
    financial_asset = models.ForeignKey(
        'FinancialAsset', on_delete=models.CASCADE, related_name='tax_files'
    )
    file = models.FileField(verbose_name=_("Tax Declaration File"),
                            upload_to=RENAME_TAX_DECLARATION_PATH.rename_folder)

    def __str__(self):
        return f"File for {self.financial_asset.company.company_title} - {self.financial_asset.year}"

    class Meta:
        verbose_name = _("Tax Declaration File")
        verbose_name_plural = _("Tax Declaration Files")


class FinancialAsset(models.Model):

    company = models.ForeignKey(
        CompanyProfile, on_delete=models.CASCADE, related_name='financial_records',
        verbose_name=_('Company'))
    year = models.PositiveIntegerField(verbose_name=_('Year'))

    capital_providing_method = models.ManyToManyField(
        LifeCycle, verbose_name=_('Life Cycles'), related_name='financial_assets')

    class Meta:
        unique_together = ('company', 'year')
        verbose_name = _('Financial Asset')
        verbose_name_plural = _('Financial Assets')

    def __str__(self):
        return f"{self.company.company_title} - {self.year}"
