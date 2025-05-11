import logging

from django.dispatch import receiver
from django.db.models.signals import post_save


from finance.models import TaxDeclarationFile, BalanceReportFile
from management.models import HumanResource
from request.models import FinanceRequest, ManagementRequest

from company.models import CompanyService


logger = logging.getLogger("request")


@receiver(post_save, sender=TaxDeclarationFile)
@receiver(post_save, sender=BalanceReportFile)
def create_finance_request(sender, instance, created, **kwargs):
    if created:
        # Log the creation event
        logger.info(
            f"New {sender.__name__} created for company: {instance.company.id}, year: {instance.year}"
        )

        try:
            service = CompanyService.objects.get(service__name="DIAGNOSTIC")
        except CompanyService.DoesNotExist:
            logger.error("Service 'DIAGNOSTIC' does not exist in CompanyService.")
            return

        finance_request_data = {
            "company": instance.company,
            "service": service,
            "subject": f"در صورت عدم تایید محتوای ارسال شده، علت را اینجا وارد کنید.",
        }

        if sender == TaxDeclarationFile:
            finance_request_data["tax_record"] = instance

        elif sender == BalanceReportFile:
            finance_request_data["balance_record"] = instance

        try:
            finance_request = FinanceRequest.objects.create(**finance_request_data)
            logger.info(
                f"FinanceRequest created: {finance_request.id} for {sender.__name__}"
            )
        except Exception as e:
            logger.error(
                f"Failed to create FinanceRequest for {sender.__name__}: {str(e)}"
            )


@receiver(post_save, sender=HumanResource)
def create_management_request(sender, instance, created, **kwargs):
    if created:
        logger.info(f"New {sender.__name__} created for company: {instance.company.id}")

        try:
            service = CompanyService.objects.get(service__name="MANAGEMENT")
        except CompanyService.DoesNotExist:
            logger.error("Service 'MANAGEMENT' does not exist in CompanyService.")
            return

        management_request_data = {
            "company": instance.company,
            "service": service,
            "subject": f"در صورت عدم تایید محتوای ارسال شده، علت را اینجا وارد کنید.",
        }
        management_request_data["human_resource_record"] = instance

        try:
            management_request = ManagementRequest.objects.create(
                **management_request_data
            )
            logger.info(
                f"ManagementRequest created: {management_request.id} for {sender.__name__}"
            )
        except Exception as e:
            logger.error(
                f"Failed to create ManagementRequest for {sender.__name__}: {str(e)}"
            )
