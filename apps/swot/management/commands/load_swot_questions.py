import json

from django.core.management.base import BaseCommand

from apps.swot.models import SWOTQuestion


class Command(BaseCommand):
    help = "Load SWOT options from the database"
    path = "apps/management/management/commands/fixtures/swot_questions.json"

    def handle(self, *args, **options):
        self.__load_swot_options()

    def __load_swot_options(self):
        try:
            questions = []
            with open(self.path, mode="r+") as file:
                data = json.load(file)
                for record in data:
                    questions.append(
                        SWOTQuestion(text=record["text"], category=record["category"])
                    )
            SWOTQuestion.objects.bulk_create(questions)
            self.stdout.write(
                self.style.SUCCESS("Successfully saved the fixture questions")
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"There was an error creating the questions: {e}")
            )
