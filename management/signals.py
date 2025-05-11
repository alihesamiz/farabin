import logging
import os

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from management.models import HumanResource, OrganizationChartBase, SWOTMatrix


logger = logging.getLogger("management")


# @receiver(post_save, sender=HumanResource)
# def start_process_personnel_excel(sender, instance, created, **kwargs):
#     if created:
#         from management.tasks import process_personnel_excel
#         logger.info(
#             "Starting the process of creating personnel information.")
#         process_personnel_excel.delay(instance.id)

#         logger.info(
#             "Process of creating personnel information started successfully.")
#         return


# @receiver(post_delete, sender=OrganizationChartBase)
# @receiver(post_delete, sender=HumanResource)
# def delete_hr_file(sender, instance, **kwargs):

#     if hasattr(instance, 'excel_file') and instance.excel_file:
#         file_path = instance.excel_file.path
#         if os.path.exists(file_path):
#             os.remove(file_path)

#     elif hasattr(instance, 'position_excel') and instance.position_excel:
#         file_path = instance.position_excel.path
#         if os.path.exists(file_path):
#             os.remove(file_path)


# @receiver(post_save, sender=SWOTMatrix)
# def swot_analysis_signal(sender, instance, created, **kwargs):
#     # if created:
#     from management.tasks import generate_swot_analysis
#     logger.info("Creating SWOT analysis.")
#     print(instance.id)
#     generate_swot_analysis.delay(instance.id)
#     logger.info("SWOT analysis created successfully.")
