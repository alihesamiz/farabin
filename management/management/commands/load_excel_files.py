from pathlib import Path

from django.core.management import BaseCommand
from django.core.files import File
from django.db import transaction
from management.models import OrganizationChart


class Command(BaseCommand):
    help: str = 'Loads excel files for the organization chart'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING(
            'Resolving Files path, be patient!'))

        script_path: Path = Path(__file__).resolve().parent
        file_path: Path = Path.joinpath(script_path / 'excel_files')

        for file in file_path.iterdir():
            if file.is_file() and file.suffix == '.xlsx':
                with transaction.atomic():
                    with file.open('rb') as f:
                        org_chart = OrganizationChart(position_excel=File(f, name=file.name))
                        org_chart.save()

                    self.stdout.write(self.style.SUCCESS(f"Uploaded: {file.name}"))

        self.stdout.write(self.style.SUCCESS("\nAll files processed successfully!"))