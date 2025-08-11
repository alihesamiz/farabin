from datetime import datetime

import jdatetime
import pandas as pd
from celery import shared_task
from django.db.transaction import atomic

from apps.salesdata.models import (
    CustomerSaleData,
    CustomerSaleFile,
    DomesticSaleData,
    DomesticSaleFile,
    ProductData,
    ProductDataFile,
    ProductLog,
    ProductLogFile,
)


def parse_persian_date(date_string):
    """Parses a Persian date string (e.g., '1403/05/01') and returns a standard date object."""
    try:
        jdate_obj = jdatetime.datetime.strptime(date_string, "%Y/%m/%d")
        return jdate_obj.togregorian().date()
    except (ValueError, TypeError):
        return None


@shared_task(queue="high_priority")
def read_domestic_file(file_instance_id):
    try:
        domestic_sale_file = DomesticSaleFile.objects.get(id=file_instance_id)
        company = domestic_sale_file.company
        file_path = domestic_sale_file.file.path

        df = pd.read_excel(
            file_path,
            engine="openpyxl",
            header=1,
            usecols=lambda col: col != "ردیف",
            dtype=str,
        )
        df.dropna(how="all", inplace=True)

        def parse_excel_date(value):
            if isinstance(value, datetime):
                return value.date()
            elif isinstance(value, str):
                return parse_persian_date(value)
            return None

        df["sold_at"] = df["تاریخ فروش"].apply(parse_excel_date)

        df["sale_method"] = df["روش فروش(حضور/انلاین)"].apply(
            lambda x: DomesticSaleData.SaleMethod.ONLINE
            if x == "انلاین"
            else DomesticSaleData.SaleMethod.OFFLINE
        )

        df["payment_method"] = df["نوع پرداخت(نقد/قسطی)"].apply(
            lambda x: DomesticSaleData.PaymentMethod.CASH
            if x == "نقد"
            else DomesticSaleData.PaymentMethod.INSTALLEMENT
        )
        data_to_create = [
            DomesticSaleData(
                company=company,
                sold_at=row["sold_at"],
                factor_number=row["شماره فاکتور"],
                customer_name=row["نام مشتری"],
                product_code=row["کد محصول"],
                product_name=row["نام محصول"],
                sold_amount=row["تعداد/مقدار (واحد اصلی)"],
                unit_price=row["قیمت واحد"],
                discount_price=row["مبلغ تخفیف"],
                sale_method=row["sale_method"],
                payment_method=row["payment_method"],
            )
            for _, row in df.iterrows()
        ]

        with atomic():
            DomesticSaleData.objects.bulk_create(data_to_create)

    except DomesticSaleFile.DoesNotExist:
        pass
    except Exception as e:
        print(f"Error processing file asynchronously: {e}")


@shared_task
def read_customer_list_file(file_instance_id):
    try:
        instance = CustomerSaleFile.objects.select_related("company").get(
            pk=file_instance_id
        )
        if not instance:
            return

        company = instance.company
        file_path = instance.file.path

        sale_area_map = {"داخلی": "d", "خارجی": "f"}
        channel_map = {
            "شبکه های اجتماعی": "so",
            "آنلاین": "on",
            "سئو": "se",
            "ایمیل": "em",
            "تلفنی": "ph",
            "نمایشگاه": "ex",
            "مردمی": "pe",
            "سایر": "ot",
        }

        df = pd.read_excel(
            file_path,
            engine="openpyxl",
            header=1,
            usecols=lambda col: col != "ردیف",
            dtype=str,
        )
        df.dropna(how="all", inplace=True)

        def parse_excel_date(value):
            if isinstance(value, datetime):
                return value.date()
            elif isinstance(value, str):
                return parse_persian_date(value)
            return None

        df["first_purchase_date"] = df["تاریخ اولین خرید"].apply(parse_excel_date)
        df["last_purchase_date"] = df["تاریخ آخرین خرید"].apply(parse_excel_date)

        df["sale_area"] = df["داخلی/خارجی"].map(sale_area_map).fillna("d")
        df["channel"] = df["کانال جذب مشتری"].map(channel_map).fillna("ot")

        data_to_create = [
            CustomerSaleData(
                company=company,
                name=row["نام شخص/شرکت"],
                sale_area=row["sale_area"],
                channel=row["channel"],
                city=row["شهر/منطقه"],
                first_purchase_date=row["first_purchase_date"],
                last_purchase_date=row["last_purchase_date"],
                description=row["توضیحات"],
            )
            for _, row in df.iterrows()
        ]

        with atomic():
            CustomerSaleData.objects.bulk_create(data_to_create)

    except Exception as e:
        print(f"Error processing customer file: {e}")


@shared_task
def read_product_logs_file(file_instance_id: int):
    try:
        instance = ProductLogFile.objects.select_related("company").get(
            pk=file_instance_id
        )
        if not instance:
            return
        company = instance.company
        file_path = instance.file.path

        df = pd.read_excel(
            file_path,
            engine="openpyxl",
            header=0,
            usecols=lambda col: col != "ردیف",
            dtype=str,
        )
        df.dropna(how="all", inplace=True)

        def parse_excel_date(value):
            if isinstance(value, datetime):
                return value.date()
            elif isinstance(value, str):
                return parse_persian_date(value)
            return None

        df["production_date"] = df["تاریخ تولید"].apply(parse_excel_date)

        data_to_create = [
            ProductLog(
                company=company,
                product_name=row.get("نام محصول"),
                production_date=row.get("production_date"),
                total_produced=row.get("تعداد کل تولید"),
                total_returned=row.get("تعداد محصولات برگشتی"),
                total_rejected=row.get("تعداد محصولات رد شده"),
                unit_price=row.get("قیمت محصول"),
            )
            for _, row in df.iterrows()
        ]

        with atomic():
            ProductLog.objects.bulk_create(data_to_create)

    except Exception as e:
        print(f"Error product log file: {e}")


@shared_task
def read_product_data_file(file_instance_id: int):
    try:
        instance = ProductDataFile.objects.get(pk=file_instance_id)
        company = instance.company
        file_path = instance.file.path

        df = pd.read_excel(
            file_path,
            header=1,
            usecols=lambda col: col != "ردیف",
            engine="openpyxl",
            dtype=str,
        )

        df.dropna(how="all", inplace=True)

        unit_map = {
            "متر طول": "me",
            "متر مربع": "sm",
            "گرم": "g",
            "کیلوگرم": "kg",
            "تن": "t",
            "عدد": "n",
            "سی سی": "cc",
            "لیتر": "l",
            "ساعت": "h",
            "دقیقه": "mi",
            "سایر": "o",
        }

        df["unit"] = df["واحد اصلی"].str.strip().map(unit_map).fillna("o")

        data_to_create = [
            ProductData(
                company=company,
                code=row.get("کد محصول/خدمت", ""),
                name=row.get("نام محصول/خدمات", ""),
                unit=row["unit"],
                description=row.get("توضیحات", ""),
            )
            for _, row in df.iterrows()
        ]
        with atomic():
            ProductData.objects.bulk_create(data_to_create)

    except Exception as e:
        print(f"Error product data file: {e}")
