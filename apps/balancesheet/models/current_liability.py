from django.db import models

# Default debit item - POSITIVE
def default_debit():
    return {"type": "debit", "amount": 0}

# Default credit item - NEGATIVE
def default_credit():
    return {"type": "credit", "amount": 0}


#################################
# Node 1
class CurrentLiability(models.Model):
    balance_sheet = models.OneToOneField('BalanceSheet', on_delete=models.CASCADE, related_name="current_liabilities", db_index=True)
    total_amount = models.BigIntegerField(default=0)

    class Meta:
        verbose_name = "بدهی‌ جاری - [ 3 ]"
        verbose_name_plural = "کل بدهی‌های جاری  - [ 3 ]"


# Node 2
class TradeAccountsPayable(models.Model):  # حساب ها و اسناد پرداختنی تجاری
    current_liability = models.OneToOneField(CurrentLiability, on_delete=models.CASCADE, related_name="trade_accounts_payable_items", verbose_name="بدهی جاری", db_index=True)

    domestic_suppliers = models.JSONField(default=default_credit, verbose_name="حساب ها و اسناد پرداختنی به تامین کننده داخلی")
    foreign_suppliers = models.JSONField(default=default_credit, verbose_name="حساب ها و اسناد پرداختنی به تامین کننده خارجی")


    class Meta:
        verbose_name = "حساب ها و اسناد پرداختنی تجاری - [ 30 ]"
        verbose_name_plural = "کل حساب ها و اسناد پرداختنی تجاری  - [ 30 ]"



    def total_trade_accounts_payable(self):
        return self.domestic_suppliers["amount"] + self.foreign_suppliers["amount"]


class NonTradeAccountsPayable(models.Model):  # حساب‌ها و اسناد پرداختنی غیرتجاری
    current_liability = models.OneToOneField(CurrentLiability, on_delete=models.CASCADE, related_name="non_trade_accounts_payable_items", verbose_name="بدهی جاری", db_index=True)

    salaries_payable = models.JSONField(default=default_credit, verbose_name="حقوق و دستمزد پرداختنی")
    social_security_payable = models.JSONField(default=default_credit, verbose_name="سازمان تامین اجتماعی (حق بیمه‌ی کارکنان)")
    deposits_from_entities = models.JSONField(default=default_credit, verbose_name="سپرده دریافتی از اشخاص حقیقی و حقوقی")
    deposits_from_individuals = models.JSONField(default=default_credit, verbose_name="سپرده دریافتنی از اشخاص حقیقی")
    accrued_unpaid_expenses_provision = models.JSONField(default=default_credit, verbose_name="ذخیره‌ی هزینه‌های تحقق‌یافته‌ی پرداخت‌نشده")



    class Meta:
        verbose_name = "حساب‌ها و اسناد پرداختنی غیرتجاری - [ 31 ]"
        verbose_name_plural = "کل حساب‌ها و اسناد پرداختنی غیرتجاری  - [ 31 ]"



    def total_non_trade_accounts_payable(self):
        return (
            self.salaries_payable["amount"] +
            self.social_security_payable["amount"] +
            self.deposits_from_entities["amount"] +
            self.deposits_from_individuals["amount"] +
            self.accrued_unpaid_expenses_provision["amount"]
        )


class ShareholderPayables(models.Model):  # جاری شرکا/سهامداران
    current_liability = models.OneToOneField(CurrentLiability, on_delete=models.CASCADE, related_name="shareholder_payables_items", verbose_name="بدهی جاری", db_index=True)
    amount = models.JSONField(default=default_credit, verbose_name="مبلغ")

    class Meta:
        verbose_name = "جاری شرکا/سهامداران - [ 32 ]"
        verbose_name_plural = "کل جاری شرکا/سهامداران  - [ 32 ]"


class DividendsPayable(models.Model):  # سود سهام پرداختنی
    current_liability = models.OneToOneField(CurrentLiability, on_delete=models.CASCADE, related_name="dividends_payable_items", verbose_name="بدهی جاری", db_index=True)

    dividends_payable_to_individuals = models.JSONField(default=default_credit, verbose_name="سود سهام پرداختنی به اشخاص")
    dividends_payable_to_shareholders = models.JSONField(default=default_credit, verbose_name="سود سهام پرداختنی به سهامداران")
    dividends_payable_from_previous_years = models.JSONField(default=default_credit, verbose_name="سود سهام پرداختنی سنوات گذشته")

    class Meta:
        verbose_name = "سود سهام پرداختنی - [ 33 ]"
        verbose_name_plural = "کل سود سهام پرداختنی  - [ 33 ] " 



    def total_dividends_payable(self):
        return (
            self.dividends_payable_to_individuals["amount"] +
            self.dividends_payable_to_shareholders["amount"] +
            self.dividends_payable_from_previous_years["amount"]
        )


class ShortTermLoans(models.Model):  # تسهیلات مالی دریافتی کوتاه‌مدت
    current_liability = models.OneToOneField(CurrentLiability, on_delete=models.CASCADE, related_name="short_term_loans_items", verbose_name="بدهی جاری", db_index=True)

    loans_from_banks = models.JSONField(default=default_credit, verbose_name="تسهیلات مالی دریافتی از بانک‌ها")
    loans_from_individuals = models.JSONField(default=default_credit, verbose_name="تسهیلات مالی دریافتی از اشخاص")

    class Meta:
        verbose_name = "تسهیلات مالی دریافتی کوتاه‌مدت - [ 34 ]"
        verbose_name_plural = "کل تسهیلات مالی دریافتی کوتاه‌مدت  - [ 34 ] " 



    def total_short_term_loans(self):
        return self.loans_from_banks["amount"] + self.loans_from_individuals["amount"]


class AdvancesAndDeposits(models.Model):  # پیش‌دریافت‌ها و سپرده‌ها
    current_liability = models.OneToOneField(CurrentLiability, on_delete=models.CASCADE, related_name="advances_and_deposits_items", verbose_name="بدهی جاری", db_index=True)

    advances_for_goods_sales = models.JSONField(default=default_credit, verbose_name="پیش‌دریافت فروش کالا")
    advances_for_services = models.JSONField(default=default_credit, verbose_name="پیش‌دریافت ارائه خدمات")
    advances_for_contracts = models.JSONField(default=default_credit, verbose_name="پیش‌دریافت قرارداد پیمانکاری")
    deposits_from_others = models.JSONField(default=default_credit, verbose_name="سپرده های دیگران نزد ما")


    class Meta:
        verbose_name = "پیش‌دریافت‌ها و سپرده‌ها - [ 35 ]"
        verbose_name_plural = "کل پیش‌دریافت‌ها و سپرده‌ها  - [ 35 ] " 



    def total_advances_and_deposits(self):
        return (
            self.advances_for_goods_sales["amount"] +
            self.advances_for_services["amount"] +
            self.advances_for_contracts["amount"] +
            self.deposits_from_others["amount"]
        )


class LiabilitiesRelatedToAssetsHeldForSale(models.Model):  # بدهی‌های مرتبط با دارایی‌های نگهداری‌شده برای فروش
    current_liability = models.OneToOneField(CurrentLiability, on_delete=models.CASCADE, related_name="liabilities_related_to_assets_held_for_sale_items", verbose_name="بدهی جاری", db_index=True)

    related_loans = models.JSONField(default=default_credit, verbose_name="تسهیلات دریافت شده مربوطه")
    related_major_repairs_liability = models.JSONField(default=default_credit, verbose_name="بدهی بابت تعمیرات اساسی مربوطه")
    related_deferred_tax = models.JSONField(default=default_credit, verbose_name="مالیات معوق مربوطه")
    related_expert_fees_payable = models.JSONField(default=default_credit, verbose_name="حق‌الزحمه‌ی پرداختنی کارشناس رسمی")


    class Meta:
        verbose_name = "بدهی‌های مرتبط با دارایی‌های نگهداری‌شده برای فروش - [ 36 ]"
        verbose_name_plural = "کل بدهی‌های مرتبط با دارایی‌های نگهداری‌شده برای فروشا  - [ 36 ] " 



    def total_liabilities_related_to_assets_held_for_sale(self):
        return (
            self.related_loans["amount"] +
            self.related_major_repairs_liability["amount"] +
            self.related_deferred_tax["amount"] +
            self.related_expert_fees_payable["amount"]
        )


class TaxProvision(models.Model):  # ذخیره مالیات
    current_liability = models.OneToOneField(CurrentLiability, on_delete=models.CASCADE, related_name="tax_provision_items", verbose_name="بدهی جاری", db_index=True)
    amount = models.JSONField(default=default_credit, verbose_name="مبلغ")

    class Meta:
        verbose_name = "ذخیره مالیات - [ 37 ]"
        verbose_name_plural = "کل ذخیره مالیات  - [ 37 ] " 


class TaxPayable(models.Model):  # مالیات پرداختنی
    current_liability = models.OneToOneField(CurrentLiability, on_delete=models.CASCADE, related_name="tax_payable_items", verbose_name="بدهی جاری", db_index=True)

    payroll_tax = models.JSONField(default=default_credit, verbose_name="سازمان امور مالیاتی (مالیات حقوق)")
    withholding_tax = models.JSONField(default=default_credit, verbose_name="سازمان امور مالیاتی (مالیات تکلیفی)")
    vat_payable = models.JSONField(default=default_credit, verbose_name="سازمان امور مالیاتی (مالیات ارزش افزوده)")
    income_tax_payable = models.JSONField(default=default_credit, verbose_name="سازمان امور مالیاتی (مالیات عملکرد)")

    class Meta:
        verbose_name = "مالیات پرداختنی - [ 38 ]"
        verbose_name_plural = "کل مالیات پرداختنی  - [ 38 ] " 


    def total_tax_payable(self):
        return (
            self.payroll_tax["amount"] +
            self.withholding_tax["amount"] +
            self.vat_payable["amount"] +
            self.income_tax_payable["amount"]
        )
