from django.db import models


#################################
# Node 1
class ContingentAccount(models.Model):
    balance_sheet = models.OneToOneField('BalanceSheet', on_delete=models.CASCADE, related_name="contingent_accounts")

    class Meta:
        verbose_name = " حساب انتظامی  - [ 8 ]"
        verbose_name_plural = " کل حساب‌های انتظامی  - [ 8 ]"

        
# Node 2
class ContingentAccounts(models.Model):  # حساب‌های انتظامی
    contingent_account = models.OneToOneField(
        ContingentAccount, 
        on_delete=models.CASCADE, 
        related_name="contingent_accounts_items",
        verbose_name="حساب انتظامی",
        db_index=True
    )
    our_accounts_with_others = models.BigIntegerField(default=0, verbose_name="حساب انتظامی ما نزد دیگران")
    others_accounts_with_us = models.BigIntegerField(default=0, verbose_name="حساب انتظامی دیگران نزد ما")

    class Meta:
        verbose_name = " حساب‌های انتظامی  - [ 81 ]"
        verbose_name_plural = " کل حساب‌های انتظامی  - [ 81 ]"


    def total_contingent_accounts(self):
        return self.our_accounts_with_others + self.others_accounts_with_us



# Node 2
class ContingentCounterparties(models.Model):  # طرف حساب‌های انتظامی
    contingent_account = models.OneToOneField(
        ContingentAccount, 
        on_delete=models.CASCADE, 
        related_name="contingent_counterparties_items",
        verbose_name="حساب انتظامی",
        db_index=True
    )
    our_counterparties_with_others = models.CharField(max_length=255, verbose_name="طرف حساب انتظامی ما نزد دیگران")
    others_counterparties_with_us = models.CharField(max_length=255, verbose_name="طرف حساب انتظامی دیگران نزد ما")
    amount = models.BigIntegerField(default=0, verbose_name="مبلغ")


    class Meta:
        verbose_name = " طرف حساب‌های انتظامی  - [ 82 ]"
        verbose_name_plural = " کل طرف حساب‌های انتظامی - [ 82 ]"


    def __str__(self):
        return f"{self.our_counterparties_with_others} / {self.others_counterparties_with_us} - {self.amount}"


    
