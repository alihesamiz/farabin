from django.db import models


# Default debit item - POSITIVE
def default_debit():
    return {"type": "debit", "amount": 0}

# Default credit item - NEGATIVE
def default_credit():
    return {"type": "credit", "amount": 0}



#################################
# Node 1
class Expense(models.Model):
    balance_sheet = models.OneToOneField('BalanceSheet', on_delete=models.CASCADE, related_name="expenses", db_index=True)
    total_amount = models.BigIntegerField(default=0)

    class Meta:
        verbose_name = " هزینه  - [ 7 ]"
        verbose_name_plural = " کل هزینه ها  - [ 7 ]"


# Node 2
class ProductionCosts(models.Model):  # هزینه های تولید
    expense = models.OneToOneField(Expense, on_delete=models.CASCADE, related_name="production_costs_items", verbose_name="هزینه", db_index=True)
    direct_materials = models.JSONField(default=default_debit, verbose_name="مواد مستقیم مصرفی")
    direct_labor = models.JSONField(default=default_debit, verbose_name="دستمزد مستقیم - تولید")
    machinery_depreciation = models.JSONField(default=default_debit, verbose_name="استهلاک ماشین آلات")
    production_line_insurance = models.JSONField(default=default_debit, verbose_name="بیمه خط تولید")
    energy_and_fuel = models.JSONField(default=default_debit, verbose_name="انرژی و سوخت مصرفی تولید")
    equipment_maintenance = models.JSONField(default=default_debit, verbose_name="تعمیر و نگهداری تجهیزات تولید")
    production_consumables = models.JSONField(default=default_debit, verbose_name="ابزار مصرفی تولید")
    production_rent = models.JSONField(default=default_debit, verbose_name="اجاره فضای تولید")
    raw_material_transport = models.JSONField(default=default_debit, verbose_name="حمل و نقل مواد اولیه")

    class Meta:
        verbose_name = " هزینه های تولید  - [ 71 ]"
        verbose_name_plural = " کل هزینه های تولید  - [ 71 ]"


class DistributionAndMarketingCosts(models.Model):  # هزینه‌های توزیع و فروش و بازاریابی
    expense = models.OneToOneField(Expense, on_delete=models.CASCADE, related_name="distribution_marketing_costs_items", verbose_name="هزینه", db_index=True)
    marketing_salaries = models.JSONField(default=default_debit, verbose_name="هزینه حقوق و دستمزد - بازاریابی و فروش")
    advertising_and_promotions = models.JSONField(default=default_debit, verbose_name="هزینه‌های تبلیغات، بازاریابی، کاتالوگ و بروشور")
    warehousing_costs = models.JSONField(default=default_debit, verbose_name="هزینه‌ی انبارداری")
    transportation_to_customers = models.JSONField(default=default_debit, verbose_name="حمل و نقل کالا به مشتری")
    after_sales_services = models.JSONField(default=default_debit, verbose_name="هزینه خدمات پس از فروش")
    sales_commissions = models.JSONField(default=default_debit, verbose_name="پورسانت فروش")
    packaging_and_labeling = models.JSONField(default=default_debit, verbose_name="بسته بندی و لیبل زنی")
    exhibitions_and_events = models.JSONField(default=default_debit, verbose_name="نمایشگاه ها و رویدادهای تبلیغاتی")

    class Meta:
        verbose_name = " هزینه‌های توزیع و فروش و بازاریابی  - [ 72 ]"
        verbose_name_plural = " کل هزینه‌های توزیع و فروش و بازاریابی  - [ 72 ]"


class GeneralAndAdministrativeCosts(models.Model):  # هزینه های عمومی و اداری
    expense = models.OneToOneField(Expense, on_delete=models.CASCADE, related_name="general_administrative_costs_items", verbose_name="هزینه", db_index=True)
    administrative_salaries_payable = models.JSONField(default=default_debit, verbose_name="حقوق و دستمزد پرداختنی - اداری")
    head_office_rent = models.JSONField(default=default_debit, verbose_name="اجاره دفتر مرکزی")
    utility_bills = models.JSONField(default=default_debit, verbose_name="قبوض")
    office_supplies = models.JSONField(default=default_debit, verbose_name="هزینه ملزومات")
    administrative_assets_depreciation = models.JSONField(default=default_debit, verbose_name="استهلاک دارایی های اداری")
    general_insurance = models.JSONField(default=default_debit, verbose_name="بیمه های عمومی")
    audit_and_consulting_fees = models.JSONField(default=default_debit, verbose_name="هزینه حسابرسی و مشاوره")
    hospitality_and_transport = models.JSONField(default=default_debit, verbose_name="پذیرایی و ایاب و ذهاب")

    class Meta:
        verbose_name = " هزینه های عمومی و اداری  - [ 73 ]"
        verbose_name_plural = " کل هزینه های عمومی و اداری - [ 73 ]"


class FinancialCosts(models.Model):  # هزینه‌های مالی
    expense = models.OneToOneField(Expense, on_delete=models.CASCADE, related_name="financial_costs_items", verbose_name="هزینه", db_index=True)
    bank_interest_and_fees = models.JSONField(default=default_debit, verbose_name="سود و کارمزد تسهیلات بانکی")
    loan_late_penalties = models.JSONField(default=default_debit, verbose_name="جرائم تاخیر در بازپرداخت وام")
    guarantee_fees = models.JSONField(default=default_debit, verbose_name="هزینه های کارمزد ضمانت نامه ها")
    discounting_expenses_on_receivables = models.JSONField(default=default_debit, verbose_name="هزینه های تنزیل اسناد دریافتنی")
    fund_transfer_and_bank_services = models.JSONField(default=default_debit, verbose_name="هزینه انتقال وجه و خدمات بانکی")

    class Meta:
        verbose_name = " هزینه‌های مالی  - [ 74 ]"
        verbose_name_plural = " کل هزینه‌های مالی   - [ 74 ]"


class OtherOperatingCosts(models.Model):  # سایر هزینه های عملیاتی
    expense = models.OneToOneField(Expense, on_delete=models.CASCADE, related_name="other_operating_costs_items", verbose_name="هزینه", db_index=True)
    bad_debts_and_written_off_expense = models.JSONField(default=default_debit, verbose_name="هزینه‌ی مطالبات مشکوک‌الوصول و سوخت‌شده")
    fx_non_operating_gain_loss = models.JSONField(default=default_debit, verbose_name="سود و زیان تسعیر دارایی‌ها و بدهی‌های ارزی غیرمرتبط با عملیات")
    impairment_short_term_investments = models.JSONField(default=default_debit, verbose_name="هزینه کاهش ارزش سرمایه گذاری های کوتاه مدت")
    inventory_write_down = models.JSONField(default=default_debit, verbose_name="هزینه کاهش ارزش موجودی")
    asset_impairment = models.JSONField(default=default_debit, verbose_name="هزینه کاهش ارزش دارایی")
    impairment_long_term_investments = models.JSONField(default=default_debit, verbose_name="هزینه کاهش ارزش سرمایه گذاری های بلند مدت")
    fx_operating_gain_loss = models.JSONField(default=default_debit, verbose_name="سود و زیان ناشی از تسعیر دارایی‌ها و بدهی‌های ارزی عملیاتی")

    class Meta:
        verbose_name = " سایر هزینه های عملیاتی  - [ 75 ]"
        verbose_name_plural = " کل سایر هزینه های عملیاتی  - [ 75 ]"





