
from django.db import models


# Default debit item - POSITIVE
def default_debit():
    return {"type": "debit", "amount": 0}

# Default credit item - NEGATIVE
def default_credit():
    return {"type": "credit", "amount": 0}



#################################
# Node 1
class FixedAsset(models.Model):
    balance_sheet = models.OneToOneField('BalanceSheet', on_delete=models.CASCADE, related_name="fixed_assets", db_index=True)
    total_amount = models.BigIntegerField(default=0)

    class Meta:
        verbose_name = "دارایی غیر جاری  - [ 2 ]"
        verbose_name_plural = "کل دارایی های غیر جاری - [ 2 ]"





# Node 2
class IntangibleAsset(models.Model):  # دارایی‌های نامشهود
    fixed_asset = models.OneToOneField(FixedAsset, on_delete=models.CASCADE, related_name="intangible_assets", verbose_name="دارایی ثابت", db_index=True)

    software = models.JSONField(default=default_debit, verbose_name="نرم‌افزار")
    royalty = models.JSONField(default=default_debit, verbose_name="حق الامتیاز")
    goodwill = models.JSONField(default=default_debit, verbose_name="سرقفلی")
    patent = models.JSONField(default=default_debit, verbose_name="حق اختراع")
    trademark = models.JSONField(default=default_debit, verbose_name="علائم تجاری و برندها")
    copyright = models.JSONField(default=default_debit, verbose_name="حق تالیف/ حق نشر")
    pre_operating_expenses = models.JSONField(default=default_debit, verbose_name="هزینه های قبل از بهره برداری")

    class Meta:
        verbose_name = "دارایی‌های نامشهود  - [ 20 ]"
        verbose_name_plural = "کل دارایی‌های نامشهود - [ 20 ]"


    def total_intangible_assets(self):
        return (
            self.software["amount"] +
            self.royalty["amount"] +
            self.goodwill["amount"] +
            self.patent["amount"] +
            self.trademark["amount"] +
            self.copyright["amount"] +
            self.pre_operating_expenses["amount"]
        )


class TangibleFixedAsset(models.Model):  # دارایی‌های ثابت مشهود
    fixed_asset = models.OneToOneField(FixedAsset, on_delete=models.CASCADE, related_name="tangible_fixed_assets", verbose_name="دارایی ثابت", db_index=True)

    land = models.JSONField(default=default_debit, verbose_name="زمین")
    building = models.JSONField(default=default_debit, verbose_name="ساختمان")
    installations = models.JSONField(default=default_debit, verbose_name="تاسیسات")
    machinery_and_equipment = models.JSONField(default=default_debit, verbose_name="ماشین‌آلات و تجهیزات")
    vehicles = models.JSONField(default=default_debit, verbose_name="وسایل نقلیه")
    office_furniture = models.JSONField(default=default_debit, verbose_name="اثاثیه اداری")
    accumulated_depreciation = models.JSONField(default=default_debit, verbose_name="استهلاک انباشته‌ی دارایی غیر جاری") 

    class Meta:
        verbose_name = "دارایی‌های ثابت مشهود  - [ 21 ]"
        verbose_name_plural = "کل دارایی‌های ثابت مشهود - [ 21 ]"


    def net_tangible_fixed_assets(self):
        total_assets = (
            self.land["amount"] +
            self.building["amount"] +
            self.installations["amount"] +
            self.machinery_and_equipment["amount"] +
            self.vehicles["amount"] +
            self.office_furniture["amount"]
        )
        return total_assets - self.accumulated_depreciation["amount"]


class AssetsInProgress(models.Model):  # دارایی در جریان تکمیل
    fixed_asset = models.OneToOneField(FixedAsset, on_delete=models.CASCADE, related_name="assets_in_progress", verbose_name="دارایی ثابت", db_index=True)
    amount = models.JSONField(default=default_debit, verbose_name="دارایی در جریان تکمیل")

    class Meta:
        verbose_name = "دارایی در جریان تکمیل  - [ 22 ]"
        verbose_name_plural = "دارایی در جریان تکمیل - [ 22 ]"



class LongTermInvestment(models.Model):  # سرمایه‌گذاری بلندمدت
    fixed_asset = models.OneToOneField(FixedAsset, on_delete=models.CASCADE, related_name="long_term_investments", verbose_name="دارایی ثابت", db_index=True)

    investment_in_affiliates = models.JSONField(default=default_debit, verbose_name="سرمایه گذاری در سهام شرکت های وابسته")
    investment_in_subsidiaries = models.JSONField(default=default_debit, verbose_name="سرمایه گذاری در سهام شرکت های فرعی")
    investment_in_private_companies = models.JSONField(default=default_debit, verbose_name="سرمایه گذاری در سهام شرکت های غیربورسی")
    long_term_bonds = models.JSONField(default=default_debit, verbose_name="سرمایه گذاری در اوراق مشارکت بلندمدت")
    property_investment = models.JSONField(default=default_debit, verbose_name="سرمایه گذاری بلند مدت در املاک")
    long_term_deposits = models.JSONField(default=default_debit, verbose_name="سپرده های بلند مدت")
    long_term_participation_in_projects = models.JSONField(default=default_debit, verbose_name="مشارکت بلند مدت در طرح ها و پروژه ها")
    long_term_treasury_investment = models.JSONField(default=default_debit, verbose_name="سرمایه گذاری بلند مدت در اوراق خزانه")
    long_term_investment_impairment = models.JSONField(default=default_credit, verbose_name="ذخیره کاهش ارزش سرمایه گذاری های بلند مدت")  # Negative

    class Meta:
        verbose_name = "سرمایه‌گذاری بلندمدت  - [ 23 ]"
        verbose_name_plural = "کل سرمایه‌گذاری بلندمدت - [ 23 ]"


    def total_long_term_investment(self):
        total = (
            self.investment_in_affiliates["amount"] +
            self.investment_in_subsidiaries["amount"] +
            self.investment_in_private_companies["amount"] +
            self.long_term_bonds["amount"] +
            self.property_investment["amount"] +
            self.long_term_deposits["amount"] +
            self.long_term_participation_in_projects["amount"] +
            self.long_term_treasury_investment["amount"]
        )
        return total - self.long_term_investment_impairment["amount"]


class OtherNonCurrentAsset(models.Model):  # سایر دارایی های غیر جاری
    fixed_asset = models.OneToOneField(FixedAsset, on_delete=models.CASCADE, related_name="other_non_current_assets", verbose_name="دارایی ثابت", db_index=True)
    amount = models.JSONField(default=default_debit, verbose_name="سایر دارایی های غیر جاری")

    class Meta:
        verbose_name = "سایر دارایی های غیر جاری  - [ 24 ]"
        verbose_name_plural = "کل سایر دارایی های غیر جاری - [ 24 ]"

