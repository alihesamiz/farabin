# import json
# import os
# from django.core.management.base import BaseCommand
# from ticket.models import Department

# class Command(BaseCommand):
#     help = 'load defiend services from a json if exists otherwise from this directory'

#     def handle(self, *args, **kwargs):
#         # Load the JSON data
#         script_dir = os.path.dirname(os.path.abspath(__file__))

#         # Build the full path to the JSON file
#         file_path = os.path.join(script_dir, 'departments.json')
#         with open(file_path, 'r', encoding='utf-8') as file:
#             data = json.load(file)

#             for item in data:
#                 # Access the province information
#                 department_name = item['name']
#                 department_description = item['description']
#                 # Get or create the province
#                 service, created = Department.objects.get_or_create(
#                     name=department_name,
#                     description=department_description,
#                 )

#         self.stdout.write(self.style.SUCCESS(
#             'Successfully populated Departments'))
