from django.db import models

# Default debit item - POSITIVE
def default_debit():
    return {"type": "debit", "amount": 0}

# Default credit item - NEGATIVE
def default_credit():
    return {"type": "credit", "amount": 0}


#################################
# Node 1
class Revenue(models.Model):
    balance_sheet = models.OneToOneField('BalanceSheet', on_delete=models.CASCADE, related_name="revenues", db_index=True)
    total_amount = models.BigIntegerField(default=0)

    class Meta:
        verbose_name = " درآمد  - [ 6 ]"
        verbose_name_plural = " کل درآمدها - [ 6 ]"



# Node 2
class NetSales(models.Model):  # خالص فروش
    revenue = models.OneToOneField(Revenue, on_delete=models.CASCADE, related_name="net_sales_items", verbose_name="درآمد", db_index=True)
    amount = models.JSONField(default=default_credit, verbose_name="خالص فروش")

    class Meta:
        verbose_name = " خالص فروش  - [ 61 ]"
        verbose_name_plural = " کل خالص فروش - [ 61 ]"




class ServiceRevenue(models.Model):  # درآمد ارائه خدمات
    revenue = models.OneToOneField(Revenue, on_delete=models.CASCADE, related_name="service_revenue_items", verbose_name="درآمد", db_index=True)
    amount = models.JSONField(default=default_credit, verbose_name="درآمد ارائه خدمات")

    class Meta:
        verbose_name = " درآمد ارائه خدمات  - [ 62 ]"
        verbose_name_plural = " کل درآمد ارائه خدمات - [ 62 ]"




class ForeignCurrencyRevenue(models.Model):  # درآمد تسعیر ارز
    revenue = models.OneToOneField(Revenue, on_delete=models.CASCADE, related_name="foreign_currency_revenue_items", verbose_name="درآمد", db_index=True)
    amount = models.JSONField(default=default_credit, verbose_name="درآمد تسعیر ارز")

    class Meta:
        verbose_name = " درآمد تسعیر ارز  - [ 63 ]"
        verbose_name_plural = " کل درآمد تسعیر ارز - [ 63 ]"




class OtherOperatingRevenue(models.Model):  # سایر درآمدهای عملیاتی
    revenue = models.OneToOneField(Revenue, on_delete=models.CASCADE, related_name="other_operating_revenue_items", verbose_name="درآمد", db_index=True)
    amount = models.JSONField(default=default_credit, verbose_name="سایر درآمدهای عملیاتی")
    
    class Meta:
        verbose_name = " سایر درآمدهای عملیاتی  - [ 64 ]"
        verbose_name_plural = " کل سایر درآمدهای عملیاتی - [ 64 ]"


