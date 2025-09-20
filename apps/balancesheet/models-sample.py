from django.db import models









# all 






# Parent
class BalanceSheet(models.Model):
    date = models.DateField()

    # Assets
    current_assets = models.OneToOneField('CurrentAsset', on_delete=models.CASCADE, null=True, blank=True)
    non_current_assets = models.OneToOneField('NonCurrentAsset', on_delete=models.CASCADE, null=True, blank=True)

    # Liabilities
    current_liabilities = models.OneToOneField('CurrentLiability', on_delete=models.CASCADE, null=True, blank=True)
    long_term_liabilities = models.OneToOneField('LongTermLiability', on_delete=models.CASCADE, null=True, blank=True)

    # Equity
    equity = models.OneToOneField('Equity', on_delete=models.CASCADE, null=True, blank=True)

    # Income & Expenses
    revenue = models.OneToOneField('Revenue', on_delete=models.CASCADE, null=True, blank=True)
    expense = models.OneToOneField('Expense', on_delete=models.CASCADE, null=True, blank=True)

    # Contingent Accounts
    contingent_account = models.OneToOneField('ContingentAccount', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Balance Sheet - {self.date}"





#################################
# Node 1
class CurrentAsset(models.Model):
    balance_sheet = models.ForeignKey('BalanceSheet', on_delete=models.CASCADE, related_name="current_assets")
    name = models.CharField(max_length=255, blank=True)  # optional general name
    amount = models.BigIntegerField(default=0)

# Node 2
class Cash(models.Model):  # موجودی نقد
    current_asset = models.ForeignKey(CurrentAsset, on_delete=models.CASCADE, related_name="cash_items")
    
    cash_in_hand = models.BigIntegerField(default=0)  # صندوق
    bank_balances = models.BigIntegerField(default=0)  # بانک‌ها
    petty_cash = models.BigIntegerField(default=0)  # تنخواه‌گردان‌ها
    cash_in_transit = models.BigIntegerField(default=0)  # وجوه در راه

    def total_cash(self):
        return self.cash_in_hand + self.bank_balances + self.petty_cash + self.cash_in_transit
    


# Node 2
class ShortTermInvestment(models.Model):  # سرمایه‌گذاری‌های کوتاه‌مدت
    current_asset = models.ForeignKey(CurrentAsset, on_delete=models.CASCADE, related_name="short_term_investments")
    
    short_term_deposits = models.BigIntegerField(default=0)  # سپرده‌های کوتاه مدت
    tradable_stocks = models.BigIntegerField(default=0)  # سهام بورسی قابل معامله
    participation_bonds = models.BigIntegerField(default=0)  # اوراق مشارکت
    etf_investment_fund = models.BigIntegerField(default=0)  # صندوق سرمایه گذاری قابل معامله (ETF)
    other_short_term_investments = models.BigIntegerField(default=0)  # سایر سرمایه گذاری‌های کوتاه‌مدت
    short_term_investment_impairment = models.BigIntegerField(default=0)  # ذخیره‌ی کاهش ارزش سرمایه‌گذاری‌های کوتاه‌مدت

    def total_short_term_investment(self):
        return (
            self.short_term_deposits +
            self.tradable_stocks +
            self.participation_bonds +
            self.etf_investment_fund +
            self.other_short_term_investments -
            self.short_term_investment_impairment
        )
    


# Node 2
class TradeReceivable(models.Model):  # حساب‌ها و اسناد دریافتنی تجاری
    current_asset = models.ForeignKey(CurrentAsset, on_delete=models.CASCADE, related_name="trade_receivables")
    
    trade_accounts_receivable = models.BigIntegerField(default=0)  # حساب‌های دریافتنی تجاری
    trade_notes_receivable = models.BigIntegerField(default=0)  # اسناد دریافتنی تجاری
    receivables_in_litigation = models.BigIntegerField(default=0)  # حساب‌های دریافتنی در دعاوی حقوقی
    notes_in_collection = models.BigIntegerField(default=0)  # اسناد درجریان وصول
    returned_cheques = models.BigIntegerField(default=0)  # اسناد دریافتنی واخواستی (چک‌های برگشتی مشتری)
    doubtful_receivables_provision = models.BigIntegerField(default=0)  # ذخیره‌ی مطالبات مشکوک‌الوصول

    def total_trade_receivable(self):
        """
        Calculates net trade receivables after subtracting doubtful receivables provision.
        """
        return (
            self.trade_accounts_receivable +
            self.trade_notes_receivable +
            self.receivables_in_litigation +
            self.notes_in_collection +
            self.returned_cheques -
            self.doubtful_receivables_provision
        )




# Node 2
class NonTradeReceivable(models.Model):  # حساب‌ها و اسناد دریافتنی غیرتجاری
    current_asset = models.ForeignKey(CurrentAsset, on_delete=models.CASCADE, related_name="non_trade_receivables")
    
    non_trade_accounts_receivable = models.BigIntegerField(default=0)  # حساب‌های دریافتنی غیرتجاری
    non_trade_notes_receivable = models.BigIntegerField(default=0)  # اسناد دریافتنی غیرتجاری
    employee_receivables = models.BigIntegerField(default=0)  # حساب‌های دریافتنی از کارکنان (وام و مساعده)
    director_receivables = models.BigIntegerField(default=0)  # حساب‌های دریافتنی از مدیران و اعضای هیات مدیره
    related_companies_receivables = models.BigIntegerField(default=0)  # حساب‌های دریافتنی از شرکت‌ها و اشخاص وابسته
    vat_receivable = models.BigIntegerField(default=0)  # مالیات بر ارزش افزوده
    deposits_with_others = models.BigIntegerField(default=0)  # سپرده‌های ما نزد دیگران
    dividends_receivable = models.BigIntegerField(default=0)  # سود سهام دریافتنی

    def total_non_trade_receivable(self):
        """
        Calculates total non-trade receivables.
        """
        return (
            self.non_trade_accounts_receivable +
            self.non_trade_notes_receivable +
            self.employee_receivables +
            self.director_receivables +
            self.related_companies_receivables +
            self.vat_receivable +
            self.deposits_with_others +
            self.dividends_receivable
        )



# Node 2
class ShareholderReceivable(models.Model):  # جاری شرکا/سهامداران
    current_asset = models.ForeignKey(CurrentAsset, on_delete=models.CASCADE, related_name="shareholder_receivables")
    amount = models.DecimalField(max_digits=20, decimal_places=2)





# Node 2
class Inventory(models.Model):  # موجودی مواد و کالا
    current_asset = models.ForeignKey(CurrentAsset, on_delete=models.CASCADE, related_name="inventories")
    
    raw_materials = models.BigIntegerField(default=0)  # موجودی مواد اولیه
    work_in_progress = models.BigIntegerField(default=0)  # موجودی کالای درجریان ساخت
    finished_goods = models.BigIntegerField(default=0)  # موجودی کالای ساخته شده و آماده فروش
    purchased_goods_for_sale = models.BigIntegerField(default=0)  # موجودی کالای خریداری شده جهت فروش
    spare_parts = models.BigIntegerField(default=0)  # موجودی قطعات و لوازم یدکی
    packaging_materials = models.BigIntegerField(default=0)  # موجود مواد بسته بندی
    consignment_goods_with_others = models.BigIntegerField(default=0)  # کالای امانی نزد دیگران
    idle_items = models.BigIntegerField(default=0)  # موجودی اقلام راکد
    scrap_raw_materials = models.BigIntegerField(default=0)  # موجودی ضایعات مواد اولیه
    inventory_impairment = models.BigIntegerField(default=0)  # ذخیره کاهش ارزش موجودی

    def total_inventory(self):
        """
        Calculates net inventory after deducting impairment.
        """
        return (
            self.raw_materials +
            self.work_in_progress +
            self.finished_goods +
            self.purchased_goods_for_sale +
            self.spare_parts +
            self.packaging_materials +
            self.consignment_goods_with_others +
            self.idle_items +
            self.scrap_raw_materials -
            self.inventory_impairment
        )
    


# Node 2
class OrdersAndPrepayments(models.Model):  # سفارش‌ها و پیش‌پرداخت‌ها
    current_asset = models.ForeignKey(CurrentAsset, on_delete=models.CASCADE, related_name="orders_and_prepayments")
    
    prepaid_goods_and_services = models.BigIntegerField(default=0)  # پیش‌پرداخت خرید کالا و خدمات
    prepaid_income_tax = models.BigIntegerField(default=0)  # پیش‌پرداخت مالیات عملکرد
    prepaid_rent = models.BigIntegerField(default=0)  # پیش‌پرداخت اجاره
    prepaid_insurance = models.BigIntegerField(default=0)  # پیش‌پرداخت بیمه
    orders_in_transit = models.BigIntegerField(default=0)  # سفارشات در راه
    prepaid_loans = models.BigIntegerField(default=0)  # پیش پرداخت تسهیلات
    prepaid_interest_on_loans = models.BigIntegerField(default=0)  # پیش پرداخت سود تسهیلات
    other_prepayments = models.BigIntegerField(default=0)  # سایر پیش‌پرداخت‌ها

    def total_orders_and_prepayments(self):
        """
        Calculates total of all orders and prepayments.
        """
        return (
            self.prepaid_goods_and_services +
            self.prepaid_income_tax +
            self.prepaid_rent +
            self.prepaid_insurance +
            self.orders_in_transit +
            self.prepaid_loans +
            self.prepaid_interest_on_loans +
            self.other_prepayments
        )



# Node 2
class AssetsHeldForSale(models.Model):  # دارایی نگهداری شده برای فروش
    current_asset = models.ForeignKey(CurrentAsset, on_delete=models.CASCADE, related_name="assets_held_for_sale")
    
    assets_held_for_sale = models.BigIntegerField(default=0)  # ارزش دارایی نگهداری شده برای فروش
    impairment_reserve = models.BigIntegerField(default=0)  # ذخیره کاهش ارزش دارایی

    def net_assets_held_for_sale(self):
        """
        Calculates net value of assets held for sale after impairment.
        """
        return self.assets_held_for_sale - self.impairment_reserve









#################################
# Node 1
class FixedAsset(models.Model):
    balance_sheet = models.ForeignKey(BalanceSheet, on_delete=models.CASCADE, related_name="fixed_assets")


# Node 2
class IntangibleAsset(models.Model):  # دارایی‌های نامشهود
    fixed_asset = models.ForeignKey(FixedAsset, on_delete=models.CASCADE, related_name="intangible_assets")
    
    software = models.BigIntegerField(default=0)  # نرم‌افزار
    royalty = models.BigIntegerField(default=0)  # حق الامتیاز
    goodwill = models.BigIntegerField(default=0)  # سرقفلی
    patent = models.BigIntegerField(default=0)  # حق اختراع
    trademark = models.BigIntegerField(default=0)  # علائم تجاری و برندها
    copyright = models.BigIntegerField(default=0)  # حق تالیف/ حق نشر
    pre_operating_expenses = models.BigIntegerField(default=0)  # هزینه های قبل از بهره برداری

    def total_intangible_assets(self):
        """
        Calculates total value of intangible assets.
        """
        return (
            self.software +
            self.royalty +
            self.goodwill +
            self.patent +
            self.trademark +
            self.copyright +
            self.pre_operating_expenses
        )



# Node 2
class TangibleFixedAsset(models.Model):  # دارایی‌های ثابت مشهود
    fixed_asset = models.ForeignKey(FixedAsset, on_delete=models.CASCADE, related_name="tangible_fixed_assets")
    
    land = models.BigIntegerField(default=0)  # زمین
    building = models.BigIntegerField(default=0)  # ساختمان
    installations = models.BigIntegerField(default=0)  # تاسیسات
    machinery_and_equipment = models.BigIntegerField(default=0)  # ماشین‌آلات و تجهیزات
    vehicles = models.BigIntegerField(default=0)  # وسایل نقلیه
    office_furniture = models.BigIntegerField(default=0)  # اثاثیه اداری
    accumulated_depreciation = models.BigIntegerField(default=0)  # استهلاک انباشته‌ی دارایی غیر جاری

    def net_tangible_fixed_assets(self):
        """
        Calculates net value of tangible fixed assets after accumulated depreciation.
        """
        total_assets = (
            self.land +
            self.building +
            self.installations +
            self.machinery_and_equipment +
            self.vehicles +
            self.office_furniture
        )
        return total_assets - self.accumulated_depreciation
    



# Node 2
class AssetsInProgress(models.Model):  # دارایی در جریان تکمیل
    fixed_asset = models.ForeignKey(FixedAsset, on_delete=models.CASCADE, related_name="assets_in_progress")
    amount = models.BigIntegerField(default=0)




# Node 2
class LongTermInvestment(models.Model):  # سرمایه‌گذاری بلندمدت
    fixed_asset = models.ForeignKey(FixedAsset, on_delete=models.CASCADE, related_name="long_term_investments")
    
    investment_in_affiliates = models.BigIntegerField(default=0)  # سرمایه گذاری در سهام شرکت های وابسته
    investment_in_subsidiaries = models.BigIntegerField(default=0)  # سرمایه گذاری در سهام شرکت های فرعی
    investment_in_private_companies = models.BigIntegerField(default=0)  # سرمایه گذاری در سهام شرکت های غیربورسی
    long_term_bonds = models.BigIntegerField(default=0)  # سرمایه گذاری در اوراق مشارکت بلندمدت
    property_investment = models.BigIntegerField(default=0)  # سرمایه گذاری بلند مدت در املاک
    long_term_deposits = models.BigIntegerField(default=0)  # سپرده های بلند مدت
    long_term_participation_in_projects = models.BigIntegerField(default=0)  # مشارکت بلند مدت در طرح ها و پروژه ها
    long_term_treasury_investment = models.BigIntegerField(default=0)  # سرمایه گذاری بلند مدت در اوراق خزانه
    long_term_investment_impairment = models.BigIntegerField(default=0)  # ذخیره کاهش ارزش سرمایه گذاری های بلند مدت

    def total_long_term_investment(self):
        """
        Calculates total net long-term investment after impairment.
        """
        total = (
            self.investment_in_affiliates +
            self.investment_in_subsidiaries +
            self.investment_in_private_companies +
            self.long_term_bonds +
            self.property_investment +
            self.long_term_deposits +
            self.long_term_participation_in_projects +
            self.long_term_treasury_investment
        )
        return total - self.long_term_investment_impairment



# Node 2
class OtherNonCurrentAsset(models.Model):  # سایر دارایی های غیر جاری
    fixed_asset = models.ForeignKey(FixedAsset, on_delete=models.CASCADE, related_name="other_non_current_assets")
    amount = models.BigIntegerField(default=0)








#################################
# Node 1
class CurrentLiability(models.Model):
    balance_sheet = models.ForeignKey(BalanceSheet, on_delete=models.CASCADE, related_name="current_liabilities")


# Node 2
class TradeAccountsPayable(models.Model):  # حساب ها و اسناد پرداختنی تجاری
    current_liability = models.ForeignKey(CurrentLiability, on_delete=models.CASCADE, related_name="trade_accounts_payable_items")
    
    domestic_suppliers = models.BigIntegerField(default=0)  # حساب ها و اسناد پرداختنی به تامین کننده داخلی
    foreign_suppliers = models.BigIntegerField(default=0)  # حساب ها و اسناد پرداختنی به تامین کننده خارجی

    def total_trade_accounts_payable(self):
        """
        Calculates total trade accounts payable (domestic + foreign).
        """
        return self.domestic_suppliers + self.foreign_suppliers
    



# Node 2
class NonTradeAccountsPayable(models.Model):  # حساب‌ها و اسناد پرداختنی غیرتجاری
    current_liability = models.ForeignKey(CurrentLiability, on_delete=models.CASCADE, related_name="non_trade_accounts_payable_items")
    
    salaries_payable = models.BigIntegerField(default=0)  # حقوق و دستمزد پرداختنی
    social_security_payable = models.BigIntegerField(default=0)  # سازمان تامین اجتماعی (حق بیمه‌ی کارکنان)
    deposits_from_entities = models.BigIntegerField(default=0)  # سپرده دریافتی از اشخاص حقیقی و حقوقی
    deposits_from_individuals = models.BigIntegerField(default=0)  # سپرده دریافتنی از اشخاص حقیقی
    accrued_unpaid_expenses_provision = models.BigIntegerField(default=0)  # ذخیره‌ی هزینه‌های تحقق‌یافته‌ی پرداخت‌نشده

    def total_non_trade_accounts_payable(self):
        """
        Calculates total non-trade accounts payable.
        """
        return (
            self.salaries_payable +
            self.social_security_payable +
            self.deposits_from_entities +
            self.deposits_from_individuals +
            self.accrued_unpaid_expenses_provision
        )


# Node 2
class ShareholderPayables(models.Model):  # جاری شرکا/سهامداران
    current_liability = models.ForeignKey(CurrentLiability, on_delete=models.CASCADE, related_name="shareholder_payables_items")
    amount = models.BigIntegerField(default=0)



# Node 2
class DividendsPayable(models.Model):  # سود سهام پرداختنی
    current_liability = models.ForeignKey(CurrentLiability, on_delete=models.CASCADE, related_name="dividends_payable_items")
    
    dividends_payable_to_individuals = models.BigIntegerField(default=0)  # سود سهام پرداختنی به اشخاص
    dividends_payable_to_shareholders = models.BigIntegerField(default=0)  # سود سهام پرداختنی به سهامداران
    dividends_payable_from_previous_years = models.BigIntegerField(default=0)  # سود سهام پرداختنی سنوات گذشته

    def total_dividends_payable(self):
        """
        Calculates total dividends payable.
        """
        return (
            self.dividends_payable_to_individuals +
            self.dividends_payable_to_shareholders +
            self.dividends_payable_from_previous_years
        )



# Node 2
class ShortTermLoans(models.Model):  # تسهیلات مالی دریافتی کوتاه‌مدت
    current_liability = models.ForeignKey(CurrentLiability, on_delete=models.CASCADE, related_name="short_term_loans_items")
    
    loans_from_banks = models.BigIntegerField(default=0)  # تسهیلات مالی دریافتی از بانک‌ها
    loans_from_individuals = models.BigIntegerField(default=0)  # تسهیلات مالی دریافتی از اشخاص

    def total_short_term_loans(self):
        """
        Calculates total short-term loans (banks + individuals).
        """
        return self.loans_from_banks + self.loans_from_individuals




# Node 2
class AdvancesAndDeposits(models.Model):  # پیش‌دریافت‌ها و سپرده‌ها
    current_liability = models.ForeignKey(CurrentLiability, on_delete=models.CASCADE, related_name="advances_and_deposits_items")
    
    advances_for_goods_sales = models.BigIntegerField(default=0)  # پیش‌دریافت فروش کالا
    advances_for_services = models.BigIntegerField(default=0)  # پیش‌دریافت ارائه خدمات
    advances_for_contracts = models.BigIntegerField(default=0)  # پیش‌دریافت قرارداد پیمانکاری
    deposits_from_others = models.BigIntegerField(default=0)  # سپرده های دیگران نزد ما

    def total_advances_and_deposits(self):
        """
        Calculates total of all advances and deposits.
        """
        return (
            self.advances_for_goods_sales +
            self.advances_for_services +
            self.advances_for_contracts +
            self.deposits_from_others
        )

# Node 2
class LiabilitiesRelatedToAssetsHeldForSale(models.Model):  # بدهی‌های مرتبط با دارایی‌های نگهداری‌شده برای فروش
    current_liability = models.ForeignKey(
        CurrentLiability, 
        on_delete=models.CASCADE, 
        related_name="liabilities_related_to_assets_held_for_sale_items"
    )
    
    related_loans = models.BigIntegerField(default=0)  # تسهیلات دریافت شده مربوطه
    related_major_repairs_liability = models.BigIntegerField(default=0)  # بدهی بابت تعمیرات اساسی مربوطه
    related_deferred_tax = models.BigIntegerField(default=0)  # مالیات معوق مربوطه
    related_expert_fees_payable = models.BigIntegerField(default=0)  # حق‌الزحمه‌ی پرداختنی کارشناس رسمی

    def total_liabilities_related_to_assets_held_for_sale(self):
        """
        Calculates total liabilities related to assets held for sale.
        """
        return (
            self.related_loans +
            self.related_major_repairs_liability +
            self.related_deferred_tax +
            self.related_expert_fees_payable
        )




# Node 2
class TaxProvision(models.Model):  # ذخیره مالیات
    current_liability = models.ForeignKey(CurrentLiability, on_delete=models.CASCADE, related_name="tax_provision_items")
    amount = models.BigIntegerField(default=0)



# Node 2
class TaxPayable(models.Model):  # مالیات پرداختنی
    current_liability = models.ForeignKey(
        CurrentLiability, 
        on_delete=models.CASCADE, 
        related_name="tax_payable_items"
    )
    
    payroll_tax = models.BigIntegerField(default=0)  # سازمان امور مالیاتی (مالیات حقوق)
    withholding_tax = models.BigIntegerField(default=0)  # سازمان امور مالیاتی (مالیات تکلیفی)
    vat_payable = models.BigIntegerField(default=0)  # سازمان امور مالیاتی (مالیات ارزش افزوده)
    income_tax_payable = models.BigIntegerField(default=0)  # سازمان امور مالیاتی (مالیات عملکرد)

    def total_tax_payable(self):
        """
        Calculates total tax payable.
        """
        return (
            self.payroll_tax +
            self.withholding_tax +
            self.vat_payable +
            self.income_tax_payable
        )








#########################################
# Node 1
class LongTermLiability(models.Model):
    balance_sheet = models.ForeignKey(BalanceSheet, on_delete=models.CASCADE, related_name="long_term_liabilities")




# Node 2
class LongTermAccountsPayable(models.Model):  # حساب ها و اسناد پرداختنی بلندمدت
    long_term_liability = models.ForeignKey(
        LongTermLiability, 
        on_delete=models.CASCADE, 
        related_name="long_term_accounts_payable_items"
    )
    
    long_term_notes_payable = models.BigIntegerField(default=0)  # اسناد پرداختنی بلند مدت
    long_term_accounts_payable = models.BigIntegerField(default=0)  # حساب های پرداختنی بلند مدت

    def total_long_term_accounts_payable(self):
        """
        Calculates total long-term accounts payable (notes + accounts).
        """
        return self.long_term_notes_payable + self.long_term_accounts_payable


# Node 2
class LongTermLoans(models.Model):  # تسهیلات مالی دریافتی بلندمدت از بانک‌ها
    long_term_liability = models.ForeignKey(
        LongTermLiability, 
        on_delete=models.CASCADE, 
        related_name="long_term_loans_items"
    )
    
    loans_from_banks = models.BigIntegerField(default=0)  # تسهیلات مالی دریافتی بلندمدت از بانک‌ها


# Node 2
class LongTermProvisions(models.Model):  # ذخایر بلند مدت
    long_term_liability = models.ForeignKey(
        LongTermLiability, 
        on_delete=models.CASCADE, 
        related_name="long_term_provisions_items"
    )
    
    employee_end_of_service_benefits = models.BigIntegerField(default=0)  # ذخیره‌ی مزایای پایان خدمت کارکنان





#################################
# Node 1
class Equity(models.Model):
    balance_sheet = models.ForeignKey(BalanceSheet, on_delete=models.CASCADE, related_name="equities")

# Node 2
class InitialCapital(models.Model):  # سرمایه اولیه
    equity = models.ForeignKey(Equity, on_delete=models.CASCADE, related_name="initial_capital_items")
    amount = models.BigIntegerField(default=0)


# Node 2
class CapitalIncreaseDecrease(models.Model):  # افزایش /کاهش سرمایه
    equity = models.ForeignKey(Equity, on_delete=models.CASCADE, related_name="capital_increase_decrease_items")
    amount = models.BigIntegerField(default=0)


# Node 2
class SharePremiumReserve(models.Model):  # اندوخته‌ی صرف سهام
    equity = models.ForeignKey(Equity, on_delete=models.CASCADE, related_name="share_premium_reserve_items")
    amount = models.BigIntegerField(default=0)


# Node 2
class ShareDiscountReserve(models.Model):  # اندوخته کسر سهام
    equity = models.ForeignKey(Equity, on_delete=models.CASCADE, related_name="share_discount_reserve_items")
    amount = models.BigIntegerField(default=0)


# Node 2
class LegalReserve(models.Model):  # اندوخته‌ی قانونی
    equity = models.ForeignKey(Equity, on_delete=models.CASCADE, related_name="legal_reserve_items")
    amount = models.BigIntegerField(default=0)


# Node 2
class OtherReserves(models.Model):  # سایر اندوخته‌ها
    equity = models.ForeignKey(Equity, on_delete=models.CASCADE, related_name="other_reserves_items")
    amount = models.BigIntegerField(default=0)


# Node 2
class RevaluationSurplus(models.Model):  # مازاد تجدید ارزیابی دارایی‌ها
    equity = models.ForeignKey(Equity, on_delete=models.CASCADE, related_name="revaluation_surplus_items")
    amount = models.BigIntegerField(default=0)


# Node 2
class ForeignCurrencyTranslationDifference(models.Model):  # تفاوت تسعیر ارز
    equity = models.ForeignKey(Equity, on_delete=models.CASCADE, related_name="foreign_currency_translation_difference_items")
    amount = models.BigIntegerField(default=0)


# Node 2
class RetainedEarnings(models.Model):  # سود (زیان)انباشته
    equity = models.ForeignKey(Equity, on_delete=models.CASCADE, related_name="retained_earnings_items")
    amount = models.BigIntegerField(default=0)







#################################
# Node 1
class Revenue(models.Model):
    balance_sheet = models.ForeignKey(BalanceSheet, on_delete=models.CASCADE, related_name="revenues")

# Node 2
class NetSales(models.Model):  # خالص فروش
    revenue = models.ForeignKey(Revenue, on_delete=models.CASCADE, related_name="net_sales_items")
    amount = models.BigIntegerField(default=0)


# Node 2
class ServiceRevenue(models.Model):  # درامد ارائه خدمات
    revenue = models.ForeignKey(Revenue, on_delete=models.CASCADE, related_name="service_revenue_items")
    amount = models.BigIntegerField(default=0)


# Node 2
class ForeignCurrencyRevenue(models.Model):  # درآمد تسعیر ارز
    revenue = models.ForeignKey(Revenue, on_delete=models.CASCADE, related_name="foreign_currency_revenue_items")
    amount = models.BigIntegerField(default=0)


# Node 2
class OtherOperatingRevenue(models.Model):  # سایر درآمدهای عملیاتی
    revenue = models.ForeignKey(Revenue, on_delete=models.CASCADE, related_name="other_operating_revenue_items")
    amount = models.BigIntegerField(default=0)






#################################
# Node 1
class Expense(models.Model):
    balance_sheet = models.ForeignKey(BalanceSheet, on_delete=models.CASCADE, related_name="expenses")



# Node 2
class ProductionCosts(models.Model):  # هزینه های تولید
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name="production_costs_items")
    
    direct_materials = models.BigIntegerField(default=0)  # مواد مستقیم مصرفی
    direct_labor = models.BigIntegerField(default=0)  # دستمزد مستقیم - تولید
    machinery_depreciation = models.BigIntegerField(default=0)  # استهلاک ماشین آلات
    production_line_insurance = models.BigIntegerField(default=0)  # بیمه خط تولید
    energy_and_fuel = models.BigIntegerField(default=0)  # انرژی و سوخت مصرفی تولید
    equipment_maintenance = models.BigIntegerField(default=0)  # تعمیر و نگهداری تجهیزات تولید
    production_consumables = models.BigIntegerField(default=0)  # ابزار مصرفی تولید
    production_rent = models.BigIntegerField(default=0)  # اجاره فضای تولید
    raw_material_transport = models.BigIntegerField(default=0)  # حمل و نقل مواد اولیه

    def total_production_costs(self):
        """
        Calculates total production costs.
        """
        return (
            self.direct_materials +
            self.direct_labor +
            self.machinery_depreciation +
            self.production_line_insurance +
            self.energy_and_fuel +
            self.equipment_maintenance +
            self.production_consumables +
            self.production_rent +
            self.raw_material_transport
        )



# Node 2
class DistributionAndMarketingCosts(models.Model):  # هزینه‌های توزیع و فروش و بازاریابی
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name="distribution_marketing_costs_items")
    
    marketing_salaries = models.BigIntegerField(default=0)  # هزینه حقوق و دستمزد - بازاریابی و فروش
    advertising_and_promotions = models.BigIntegerField(default=0)  # هزینه‌های تبلیغات، بازاریابی، کاتالوگ و بروشور
    warehousing_costs = models.BigIntegerField(default=0)  # هزینه‌ی انبارداری
    transportation_to_customers = models.BigIntegerField(default=0)  # حمل و نقل کالا به مشتری
    after_sales_services = models.BigIntegerField(default=0)  # هزینه خدمات پس از فروش
    sales_commissions = models.BigIntegerField(default=0)  # پورسانت فروش
    packaging_and_labeling = models.BigIntegerField(default=0)  # بسته بندی و لیبل زنی
    exhibitions_and_events = models.BigIntegerField(default=0)  # نمایشگاه ها و رویدادهای تبلیغاتی

    def total_distribution_marketing_costs(self):
        """
        Calculates total distribution and marketing costs.
        """
        return (
            self.marketing_salaries +
            self.advertising_and_promotions +
            self.warehousing_costs +
            self.transportation_to_customers +
            self.after_sales_services +
            self.sales_commissions +
            self.packaging_and_labeling +
            self.exhibitions_and_events
        )



# Node 2
class GeneralAndAdministrativeCosts(models.Model):  # هزینه های عمومی و اداری
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name="general_administrative_costs_items")
    
    administrative_salaries_payable = models.BigIntegerField(default=0)  # حقوق و دستمزد پرداختنی - اداری
    head_office_rent = models.BigIntegerField(default=0)  # اجاره دفتر مرکزی
    utility_bills = models.BigIntegerField(default=0)  # قبوض
    office_supplies = models.BigIntegerField(default=0)  # هزینه ملزومات
    administrative_assets_depreciation = models.BigIntegerField(default=0)  # استهلاک دارایی های اداری
    general_insurance = models.BigIntegerField(default=0)  # بیمه های عمومی
    audit_and_consulting_fees = models.BigIntegerField(default=0)  # هزینه حسابرسی و مشاوره
    hospitality_and_transport = models.BigIntegerField(default=0)  # پذیرایی و ایاب و ذهاب

    def total_general_administrative_costs(self):
        """
        Calculates total general and administrative costs.
        """
        return (
            self.administrative_salaries_payable +
            self.head_office_rent +
            self.utility_bills +
            self.office_supplies +
            self.administrative_assets_depreciation +
            self.general_insurance +
            self.audit_and_consulting_fees +
            self.hospitality_and_transport
        )



# Node 2
class FinancialCosts(models.Model):  # هزینه‌های مالی
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name="financial_costs_items")
    
    bank_interest_and_fees = models.BigIntegerField(default=0)  # سود و کارمزد تسهیلات بانکی
    loan_late_penalties = models.BigIntegerField(default=0)  # جرائم تاخیر در بازپرداخت وام
    guarantee_fees = models.BigIntegerField(default=0)  # هزینه های کارمزد ضمانت نامه ها
    discounting_expenses_on_receivables = models.BigIntegerField(default=0)  # هزینه های تنزیل اسناد دریافتنی
    fund_transfer_and_bank_services = models.BigIntegerField(default=0)  # هزینه انتقال وجه و خدمات بانکی

    def total_financial_costs(self):
        """
        Calculates total financial costs.
        """
        return (
            self.bank_interest_and_fees +
            self.loan_late_penalties +
            self.guarantee_fees +
            self.discounting_expenses_on_receivables +
            self.fund_transfer_and_bank_services
        )



# Node 2
class OtherOperatingCosts(models.Model):  # سایر هزینه های عملیاتی
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name="other_operating_costs_items")
    
    bad_debts_and_written_off_expense = models.BigIntegerField(default=0)  # هزینه‌ی مطالبات مشکوک‌الوصول و سوخت‌شده
    fx_non_operating_gain_loss = models.BigIntegerField(default=0)  # سود و زیان تسعیر دارایی‌ها و بدهی‌های ارزی غیرمرتبط با عملیات
    impairment_short_term_investments = models.BigIntegerField(default=0)  # هزینه کاهش ارزش سرمایه گذاری های کوتاه مدت
    inventory_write_down = models.BigIntegerField(default=0)  # هزینه کاهش ارزش موجودی
    asset_impairment = models.BigIntegerField(default=0)  # هزینه کاهش ارزش دارایی
    impairment_long_term_investments = models.BigIntegerField(default=0)  # هزینه کاهش ارزش سرمایه گذاری های بلند مدت
    fx_operating_gain_loss = models.BigIntegerField(default=0)  # سود و زیان ناشی از تسعیر دارایی‌ها و بدهی‌های ارزی عملیاتی

    def total_other_operating_costs(self):
        """
        Calculates total of all other operating costs.
        """
        return (
            self.bad_debts_and_written_off_expense +
            self.fx_non_operating_gain_loss +
            self.impairment_short_term_investments +
            self.inventory_write_down +
            self.asset_impairment +
            self.impairment_long_term_investments +
            self.fx_operating_gain_loss
        )






#################################
# Node 1
class ContingentAccount(models.Model):
    balance_sheet = models.ForeignKey(BalanceSheet, on_delete=models.CASCADE, related_name="contingent_accounts")


# Node 2
class ContingentAccounts(models.Model):  # حساب‌های انتظامی
    contingent_account = models.ForeignKey(
        ContingentAccount, 
        on_delete=models.CASCADE, 
        related_name="contingent_accounts_items"
    )
    
    our_accounts_with_others = models.BigIntegerField(default=0)  # حساب انتظامی ما نزد دیگران
    others_accounts_with_us = models.BigIntegerField(default=0)  # حساب انتظامی دیگران نزد ما

    def total_contingent_accounts(self):
        """
        Calculates total contingent accounts (both directions).
        """
        return self.our_accounts_with_others + self.others_accounts_with_us



# Node 2
class ContingentCounterparties(models.Model):  # طرف حساب‌های انتظامی
    contingent_account = models.ForeignKey(
        ContingentAccount, 
        on_delete=models.CASCADE, 
        related_name="contingent_counterparties_items"
    )
    
    our_counterparties_with_others = models.CharField(max_length=255)  # طرف حساب انتظامی ما نزد دیگران
    others_counterparties_with_us = models.CharField(max_length=255)  # طرف حساب انتظامی دیگران نزد ما
    amount = models.BigIntegerField(default=0)

    def __str__(self):
        return f"{self.our_counterparties_with_others} / {self.others_counterparties_with_us} - {self.amount}"