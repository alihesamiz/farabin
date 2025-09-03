from django.db.models.signals import post_save
from django.dispatch import receiver
from company.models import  CompanyUser
from core.models import User


# @receiver(post_save, sender=User)
# def create_company_for_user(sender, instance, created, **kwargs):
#     if not CompanyUser.filter(user=instance).exists():
#         company = CompanyUser.objects.create(
#                 User = instance, 
#                 company = None,
#                 # Add other nullable fields as needed
#             )
#         company.save()