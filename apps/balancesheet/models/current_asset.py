from django.db import models


# Default debit item - POSITIVE
def default_debit():
    return {"type": "debit", "amount": 0}

# Default credit item - NEGATIVE
def default_credit():
    return {"type": "credit", "amount": 0}


#################################
# Node 1
class CurrentAsset(models.Model):
    balance_sheet = models.OneToOneField('BalanceSheet', on_delete=models.CASCADE, related_name="current_assets_cash", db_index=True)

    class Meta:
        verbose_name = " دارایی‌ جاری - [ 1 ]"
        verbose_name_plural = " کل دارایی‌های جاری  - [ 1 ]"


    def total_amount(self):
        pass



# Node 2
class Cash(models.Model):  # موجودی نقد
    current_asset = models.OneToOneField(CurrentAsset, on_delete=models.CASCADE, related_name="cash_items", verbose_name="دارایی جاری", db_index=True)

    cash_in_hand = models.JSONField(default=default_debit, verbose_name=" [ 1101 ] صندوق")
    bank_balances = models.JSONField(default=default_debit, verbose_name="[ 1102 ] بانک‌ها")
    petty_cash = models.JSONField(default=default_debit, verbose_name="[ 1103 ] تنخواه‌گردان‌ها")
    cash_in_transit = models.JSONField(default=default_debit, verbose_name="[ 1104 ] وجوه در راه")


    class Meta: 
        verbose_name = "موجودی نقد  - [ 11 ] "
        verbose_name_plural = "کل موجودی نقد  - [ 11 ] "



    def total_amount(self):
        return (
            self.cash_in_hand["amount"] +
            self.bank_balances["amount"] +
            self.petty_cash["amount"] +
            self.cash_in_transit["amount"]
        )


class ShortTermInvestment(models.Model):  # سرمایه‌گذاری‌های کوتاه‌مدت
    current_asset = models.OneToOneField(CurrentAsset, on_delete=models.CASCADE, related_name="short_term_investments", verbose_name="دارایی جاری", db_index=True)

    short_term_deposits = models.JSONField(default=default_debit, verbose_name="سپرده‌های کوتاه مدت [ 1201 ] ")
    tradable_stocks = models.JSONField(default=default_debit, verbose_name="سهام بورسی قابل معامله[ 1202 ]")
    participation_bonds = models.JSONField(default=default_debit, verbose_name="[ 1203 ]اوراق مشارکت")
    etf_investment_fund = models.JSONField(default=default_debit, verbose_name="[ 1204 ]صندوق سرمایه گذاری قابل معامله (ETF)")
    other_short_term_investments = models.JSONField(default=default_debit, verbose_name="[ 1205 ]سایر سرمایه گذاری‌های کوتاه‌مدت")
    short_term_investment_impairment = models.JSONField(default=default_credit, verbose_name="[ 1206 ]ذخیره‌ی کاهش ارزش سرمایه‌گذاری‌های کوتاه‌مدت")  # Negative


    class Meta:
        verbose_name = " سرمایه‌گذاری‌های کوتاه‌مدت - [ 12 ]"
        verbose_name_plural = " کل سرمایه‌گذاری‌های کوتاه‌مدت  - [ 12 ]"


    def total_short_term_investment(self):
        return (
            self.short_term_deposits["amount"] +
            self.tradable_stocks["amount"] +
            self.participation_bonds["amount"] +
            self.etf_investment_fund["amount"] +
            self.other_short_term_investments["amount"] -
            self.short_term_investment_impairment["amount"]
        )


class TradeReceivable(models.Model):  # حساب‌ها و اسناد دریافتنی تجاری
    current_asset = models.OneToOneField(CurrentAsset, on_delete=models.CASCADE, related_name="trade_receivables", verbose_name="دارایی جاری", db_index=True)

    trade_accounts_receivable = models.JSONField(default=default_debit, verbose_name="[ 1301 ]حساب‌های دریافتنی تجاری")
    trade_notes_receivable = models.JSONField(default=default_debit, verbose_name="[ 1302 ]اسناد دریافتنی تجاری")
    receivables_in_litigation = models.JSONField(default=default_debit, verbose_name="[ 1303 ]حساب‌های دریافتنی در دعاوی حقوقی")
    notes_in_collection = models.JSONField(default=default_debit, verbose_name="[ 1304 ]اسناد درجریان وصول")
    returned_cheques = models.JSONField(default=default_debit, verbose_name="[ 1305 ]اسناد دریافتنی واخواستی (چک‌های برگشتی مشتری)")
    doubtful_receivables_provision = models.JSONField(default=default_debit, verbose_name="[ 1306 ]ذخیره‌ی مطالبات مشکوک‌الوصول")  # You can change to default_credit if needed


    class Meta:
        verbose_name = " حساب‌ها و اسناد دریافتنی تجاری - [ 13 ]"
        verbose_name_plural = " کل حساب‌ها و اسناد دریافتنی تجاری  - [ 13 ]"


    def total_trade_receivable(self):
        return (
            self.trade_accounts_receivable["amount"] +
            self.trade_notes_receivable["amount"] +
            self.receivables_in_litigation["amount"] +
            self.notes_in_collection["amount"] +
            self.returned_cheques["amount"] -
            self.doubtful_receivables_provision["amount"]
        )


class NonTradeReceivable(models.Model):  # حساب‌ها و اسناد دریافتنی غیرتجاری
    current_asset = models.OneToOneField(CurrentAsset, on_delete=models.CASCADE, related_name="non_trade_receivables", verbose_name="دارایی جاری", db_index=True)

    non_trade_accounts_receivable = models.JSONField(default=default_debit, verbose_name="[ 1401 ]حساب‌های دریافتنی غیرتجاری")
    non_trade_notes_receivable = models.JSONField(default=default_debit, verbose_name="[ 1402 ]اسناد دریافتنی غیرتجاری")
    employee_receivables = models.JSONField(default=default_debit, verbose_name="[ 1403 ]حساب‌های دریافتنی از کارکنان (وام و مساعده)")
    director_receivables = models.JSONField(default=default_debit, verbose_name="[ 1404 ]حساب‌های دریافتنی از مدیران و اعضای هیات مدیره")
    related_companies_receivables = models.JSONField(default=default_debit, verbose_name="[ 1405 ]حساب‌های دریافتنی از شرکت‌ها و اشخاص وابسته")
    vat_receivable = models.JSONField(default=default_debit, verbose_name="[ 1406 ]مالیات بر ارزش افزوده")
    deposits_with_others = models.JSONField(default=default_debit, verbose_name="[ 1407 ]سپرده‌های ما نزد دیگران")
    dividends_receivable = models.JSONField(default=default_debit, verbose_name="[ 1408 ]سود سهام دریافتنی")



    class Meta:
        verbose_name = " حساب‌ها و اسناد دریافتنی غیرتجاری - [ 14 ]"
        verbose_name_plural = " کل حساب‌ها و اسناد دریافتنی غیرتجاری  - [ 14 ]"



    def total_non_trade_receivable(self):
        return (
            self.non_trade_accounts_receivable["amount"] +
            self.non_trade_notes_receivable["amount"] +
            self.employee_receivables["amount"] +
            self.director_receivables["amount"] +
            self.related_companies_receivables["amount"] +
            self.vat_receivable["amount"] +
            self.deposits_with_others["amount"] +
            self.dividends_receivable["amount"]
        )



class ShareholderReceivable(models.Model):  # جاری شرکا/سهامداران
    current_asset = models.OneToOneField(CurrentAsset, on_delete=models.CASCADE, related_name="shareholder_receivables", verbose_name="دارایی جاری", db_index=True)
    amount = models.JSONField(default=default_debit, verbose_name="[ 1501 ]مبلغ")


    class Meta:
        verbose_name = " جاری شرکا/سهامداران - [ 15 ]"
        verbose_name_plural = " کل جاری شرکا/سهامداران  - [ 15 ]"



class Inventory(models.Model):  # موجودی مواد و کالا
    current_asset = models.OneToOneField(CurrentAsset, on_delete=models.CASCADE, related_name="inventories", verbose_name="دارایی جاری", db_index=True)

    raw_materials = models.JSONField(default=default_debit, verbose_name="[ 1601 ]موجودی مواد اولیه")
    work_in_progress = models.JSONField(default=default_debit, verbose_name="[ 1602 ]موجودی کالای درجریان ساخت")
    finished_goods = models.JSONField(default=default_debit, verbose_name="[ 1603 ]موجودی کالای ساخته شده و آماده فروش")
    purchased_goods_for_sale = models.JSONField(default=default_debit, verbose_name="[ 1604 ]موجودی کالای خریداری شده جهت فروش")
    spare_parts = models.JSONField(default=default_debit, verbose_name="[ 1605 ]موجودی قطعات و لوازم یدکی")
    packaging_materials = models.JSONField(default=default_debit, verbose_name="[ 1606 ]موجود مواد بسته بندی")
    consignment_goods_with_others = models.JSONField(default=default_debit, verbose_name="کالای امانی نزد دیگران")
    idle_items = models.JSONField(default=default_debit, verbose_name="[ 1607 ]موجودی اقلام راکد")
    scrap_raw_materials = models.JSONField(default=default_debit, verbose_name="[ 1608 ]موجودی ضایعات مواد اولیه")
    inventory_impairment = models.JSONField(default=default_credit, verbose_name="[ 1609 ]ذخیره کاهش ارزش موجودی")  # Negative


    class Meta:
        verbose_name = " موجودی مواد و کالا - [ 16 ]"
        verbose_name_plural = " کل موجودی مواد و کالا  - [ 16 ]"



    def total_inventory(self):
        return (
            self.raw_materials["amount"] +
            self.work_in_progress["amount"] +
            self.finished_goods["amount"] +
            self.purchased_goods_for_sale["amount"] +
            self.spare_parts["amount"] +
            self.packaging_materials["amount"] +
            self.consignment_goods_with_others["amount"] +
            self.idle_items["amount"] +
            self.scrap_raw_materials["amount"] -
            self.inventory_impairment["amount"]
        )


class OrdersAndPrepayments(models.Model):  # سفارش‌ها و پیش‌پرداخت‌ها
    current_asset = models.OneToOneField(CurrentAsset, on_delete=models.CASCADE, related_name="orders_and_prepayments", verbose_name="دارایی جاری", db_index=True)

    prepaid_goods_and_services = models.JSONField(default=default_debit, verbose_name="[ 1701 ]پیش‌پرداخت خرید کالا و خدمات")
    prepaid_income_tax = models.JSONField(default=default_debit, verbose_name="[ 1702 ]پیش‌پرداخت مالیات عملکرد")
    prepaid_rent = models.JSONField(default=default_debit, verbose_name="[ 1703 ]پیش‌پرداخت اجاره")
    prepaid_insurance = models.JSONField(default=default_debit, verbose_name="[ 1704 ]پیش‌پرداخت بیمه")
    orders_in_transit = models.JSONField(default=default_debit, verbose_name="[ 1705 ]سفارشات در راه")
    prepaid_loans = models.JSONField(default=default_debit, verbose_name="[ 1706 ]پیش پرداخت تسهیلات")
    prepaid_interest_on_loans = models.JSONField(default=default_debit, verbose_name="[ 1707 ]پیش پرداخت سود تسهیلات")
    other_prepayments = models.JSONField(default=default_debit, verbose_name="[ 1708 ]سایر پیش‌پرداخت‌ها")


    class Meta:
        verbose_name = " سفارش‌ها و پیش‌پرداخت‌ها - [ 17 ]"
        verbose_name_plural = " کل سفارش‌ها و پیش‌پرداخت‌ها  - [ 17 ]"



    def total_orders_and_prepayments(self):
        return (
            self.prepaid_goods_and_services["amount"] +
            self.prepaid_income_tax["amount"] +
            self.prepaid_rent["amount"] +
            self.prepaid_insurance["amount"] +
            self.orders_in_transit["amount"] +
            self.prepaid_loans["amount"] +
            self.prepaid_interest_on_loans["amount"] +
            self.other_prepayments["amount"]
        )


class AssetsHeldForSale(models.Model):  # دارایی نگهداری شده برای فروش
    current_asset = models.OneToOneField(CurrentAsset, on_delete=models.CASCADE, related_name="assets_held_for_sale", verbose_name="دارایی جاری", db_index=True)

    assets_held_for_sale = models.JSONField(default=default_debit, verbose_name="[ 1801 ]ارزش دارایی نگهداری شده برای فروش")
    impairment_reserve = models.JSONField(default=default_credit, verbose_name="[ 1802 ]ذخیره کاهش ارزش دارایی")  # Negative

    class Meta:
        verbose_name = " دارایی نگهداری شده برای فروش - [ 18 ]"
        verbose_name_plural = " کل دارایی نگهداری شده برای فروش  - [ 18 ]"



    def net_assets_held_for_sale(self):
        return self.assets_held_for_sale["amount"] - self.impairment_reserve["amount"]