from django.db import models

# Default debit item - POSITIVE
def default_debit():
    return {"type": "debit", "amount": 0}

# Default credit item - NEGATIVE
def default_credit():
    return {"type": "credit", "amount": 0}


#################################
# Node 1
class Equity(models.Model):
    balance_sheet = models.OneToOneField('BalanceSheet', on_delete=models.CASCADE, related_name="equities", db_index=True)
    total_amount = models.BigIntegerField(default=0)

    class Meta:
        verbose_name = "حقوق صاحبان سهام  - [ 5 ]"
        verbose_name_plural = " کل حقوق صاحبان سهام  - [ 5 ]"


# Node 2
class InitialCapital(models.Model):  # سرمایه اولیه
    equity = models.OneToOneField(Equity, on_delete=models.CASCADE, related_name="initial_capital_items", verbose_name="حقوق صاحبان سهام", db_index=True)
    amount = models.JSONField(default=default_credit, verbose_name="سرمایه اولیه")  # Negative

    class Meta:
        verbose_name = "سرمایه اولیه - [ 51 ]"
        verbose_name_plural = " کل سرمایه اولیه - [ 51 ]"




class CapitalIncreaseDecrease(models.Model):  # افزایش /کاهش سرمایه
    equity = models.OneToOneField(Equity, on_delete=models.CASCADE, related_name="capital_increase_decrease_items", verbose_name="حقوق صاحبان سهام", db_index=True)
    amount = models.JSONField(default=default_credit, verbose_name="افزایش / کاهش سرمایه")  # Negative

    class Meta:
        verbose_name = "افزایش /کاهش سرمایه  - [ 52 ]"
        verbose_name_plural = " کل افزایش /کاهش سرمایه  - [ 52 ]"


class SharePremiumReserve(models.Model):  # اندوخته‌ی صرف سهام
    equity = models.OneToOneField(Equity, on_delete=models.CASCADE, related_name="share_premium_reserve_items", verbose_name="حقوق صاحبان سهام", db_index=True)
    amount = models.JSONField(default=default_debit, verbose_name="اندوخته‌ی صرف سهام")  # POSITIVE

    class Meta:
        verbose_name = "اندوخته‌ی صرف سهام  - [ 53 ]"
        verbose_name_plural = " کل اندوخته‌ی صرف سهام - [ 53 ]"


class ShareDiscountReserve(models.Model):  # اندوخته کسر سهام
    equity = models.OneToOneField(Equity, on_delete=models.CASCADE, related_name="share_discount_reserve_items", verbose_name="حقوق صاحبان سهام", db_index=True)
    amount = models.JSONField(default=default_credit, verbose_name="اندوخته کسر سهام")  # Negative

    class Meta:
        verbose_name = "اندوخته کسر سهام  - [ 54 ]"
        verbose_name_plural = " کل اندوخته کسر سهام - [ 54 ]"


class LegalReserve(models.Model):  # اندوخته‌ی قانونی
    equity = models.OneToOneField(Equity, on_delete=models.CASCADE, related_name="legal_reserve_items", verbose_name="حقوق صاحبان سهام", db_index=True)
    amount = models.JSONField(default=default_debit, verbose_name="اندوخته‌ی قانونی")  # POSITIVE

    class Meta:
        verbose_name = "اندوخته‌ی قانونی  - [ 55 ]"
        verbose_name_plural = " کل اندوخته‌ی قانونی  - [ 55 ]"



class OtherReserves(models.Model):  # سایر اندوخته‌ها
    equity = models.OneToOneField(Equity, on_delete=models.CASCADE, related_name="other_reserves_items", verbose_name="حقوق صاحبان سهام", db_index=True)
    amount = models.JSONField(default=default_credit, verbose_name="سایر اندوخته‌ها")  # Negative

    class Meta:
        verbose_name = "سایر اندوخته‌ها  - [ 56 ]"
        verbose_name_plural = " کل سایر اندوخته‌ها  - [ 56 ]"


class RevaluationSurplus(models.Model):  # مازاد تجدید ارزیابی دارایی‌ها
    equity = models.OneToOneField(Equity, on_delete=models.CASCADE, related_name="revaluation_surplus_items", verbose_name="حقوق صاحبان سهام", db_index=True)
    amount = models.JSONField(default=default_credit, verbose_name="مازاد تجدید ارزیابی دارایی‌ها")  # Negative

    class Meta:
        verbose_name = "مازاد تجدید ارزیابی دارایی‌ها  - [ 57 ]"
        verbose_name_plural = " کل مازاد تجدید ارزیابی دارایی‌ها  - [ 57 ]"


class ForeignCurrencyTranslationDifference(models.Model):  # تفاوت تسعیر ارز
    equity = models.OneToOneField(Equity, on_delete=models.CASCADE, related_name="foreign_currency_translation_difference_items", verbose_name="حقوق صاحبان سهام", db_index=True)
    amount = models.JSONField(default=default_credit, verbose_name="تفاوت تسعیر ارز")  # Negative

    class Meta:
        verbose_name = "تفاوت تسعیر ارز  - [ 58 ]"
        verbose_name_plural = " کل تفاوت تسعیر ارز  - [ 58 ]"


class RetainedEarnings(models.Model):  # سود (زیان)انباشته
    equity = models.OneToOneField(Equity, on_delete=models.CASCADE, related_name="retained_earnings_items", verbose_name="حقوق صاحبان سهام", db_index=True)

    amount = models.JSONField(default=default_credit, verbose_name="سود (زیان) انباشته")  # Negative
    class Meta:
        verbose_name = "سود (زیان)انباشته  - [ 59 ]"
        verbose_name_plural = " کل سود (زیان)انباشته  - [ 59 ]"





