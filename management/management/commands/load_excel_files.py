from pathlib import Path

from django.core.management import BaseCommand
from django.core.files import File
from django.db import transaction


from management.models import OrganizationChartBase


class Command(BaseCommand):
    help: str = "Loads excel files for the organization chart"
    path: Path = Path(__file__).resolve().parent / "fixtures" / "excels"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING(
            "Resolving Files path, be patient!"))
        self.__load_excel_files()

    def __load_excel_files(self):
        for file in self.path.iterdir():
            if file.is_file() and file.suffix == ".xlsx":
                db_file = OrganizationChartBase.objects.get(
                    field=file.name.split(".")[0]
                ) if OrganizationChartBase.objects.exists() else False

                if not db_file:
                    with transaction.atomic():
                        with file.open("rb") as f:
                            org_chart = OrganizationChartBase(
                                position_excel=File(f, name=file.name),
                                field=file.name.split(".")[0],
                            )
                            org_chart.save()

                    self.stdout.write(self.style.SUCCESS(
                        f"Uploaded: {file.name}"))
                else:
                    self.stdout.write(
                        self.style.ERROR(
                            f"File With name {file.name} already exists")
                    )
        self.stdout.write(self.style.SUCCESS(
            "All files processed successfully!"))
