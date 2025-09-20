from django.db import models


# Default debit item - POSITIVE
def default_debit():
    return {"type": "debit", "amount": 0}

# Default credit item - NEGATIVE
def default_credit():
    return {"type": "credit", "amount": 0}



#########################################
# Node 1
class LongTermLiability(models.Model):
    balance_sheet = models.OneToOneField('BalanceSheet', on_delete=models.CASCADE, related_name="long_term_liabilities", db_index=True)
    total_amount = models.BigIntegerField(default=0)

    class Meta:
        verbose_name = " بدهی‌ بلندمدت  - [ 4 ]"
        verbose_name_plural = " کل بدهی‌های بلندمدت  - [ 4 ]"




# Node 2
class LongTermAccountsPayable(models.Model):  # حساب ها و اسناد پرداختنی بلندمدت
    long_term_liability = models.OneToOneField(
        LongTermLiability, 
        on_delete=models.CASCADE, 
        related_name="long_term_accounts_payable_items",
        verbose_name="بدهی بلندمدت",
        db_index=True
    )
    long_term_notes_payable = models.JSONField(default=default_credit, verbose_name="اسناد پرداختنی بلند مدت")
    long_term_accounts_payable = models.JSONField(default=default_credit, verbose_name="حساب های پرداختنی بلند مدت")

    class Meta:
        verbose_name = " حساب ها و اسناد پرداختنی بلندمدت  - [ 40 ]"
        verbose_name_plural = " کل حساب ها و اسناد پرداختنی بلندمدت  - [ 40 ]"


    def total_long_term_accounts_payable(self):
        return self.long_term_notes_payable["amount"] + self.long_term_accounts_payable["amount"]


class LongTermLoans(models.Model):  # تسهیلات مالی دریافتی بلندمدت از بانک‌ها
    long_term_liability = models.OneToOneField(
        LongTermLiability, 
        on_delete=models.CASCADE, 
        related_name="long_term_loans_items",
        verbose_name="بدهی بلندمدت",
        db_index=True
    )
    loans_from_banks = models.JSONField(default=default_credit, verbose_name="تسهیلات مالی دریافتی بلندمدت از بانک‌ها")

    class Meta:
        verbose_name = " تسهیلات مالی دریافتی بلندمدت از بانک‌ها  - [ 41 ]"
        verbose_name_plural = " کل تسهیلات مالی دریافتی بلندمدت از بانک‌ها - [ 41 ]"




class LongTermProvisions(models.Model):  # ذخایر بلند مدت
    long_term_liability = models.OneToOneField(
        LongTermLiability, 
        on_delete=models.CASCADE, 
        related_name="long_term_provisions_items",
        verbose_name="بدهی بلندمدت"
        , db_index=True
    )
    employee_end_of_service_benefits = models.JSONField(default=default_credit, verbose_name="ذخیره‌ی مزایای پایان خدمت کارکنان")

    class Meta:
        verbose_name = " ذخایر بلند مدت  - [ 42 ]"
        verbose_name_plural = " کل ذخایر بلند مدت  - [ 42 ]"


