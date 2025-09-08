from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel


class QuestionMetric(TimeStampedModel):
    question = models.ForeignKey(
        "Question",  # CHANGED: Was "QuestionChoice"
        on_delete=models.CASCADE,
        related_name="metrics",  # CHANGED: Plural and more descriptive
        verbose_name=_("سوال"),
    )
    title = models.CharField(verbose_name=_("Title"), max_length=128)
    weight = models.DecimalField(
        verbose_name=_("Weight"), max_digits=4, decimal_places=2
    )

    class Meta:
        verbose_name = _("شاخص سوال")
        verbose_name_plural = _("شاخص‌های سوالات")
        # ADDED: Ensure a question doesn't have the same metric twice.
        constraints = [
            models.UniqueConstraint(fields=["question", "title"], name="unique_question_metric")
        ]

    def __str__(self):
        return f"{self.title!s}"


class QuestionChoice(models.Model):
    question = models.ForeignKey(
        "Question",
        on_delete=models.CASCADE,
        related_name="choices",
        verbose_name=_("سوال"),
    )
    answer = models.CharField(max_length=128, verbose_name=_("پاسخ"))
    points = models.IntegerField(verbose_name=_("امتیاز"))

    class Meta:
        verbose_name = _("گزینه‌ سوال")
        verbose_name_plural = _("گزینه‌های سوالات")

    def __str__(self):
        return f"{self.answer} ({self.points} امتیاز)"


class Question(TimeStampedModel):
    text = models.CharField(max_length=255, verbose_name=_("سوال"))

    class Meta:
        verbose_name = _("سوال")
        verbose_name_plural = _("سوالات")

    def __str__(self):
        return f"{self.text!s}"


# No changes to Questionnaire or QuestionnaireQuestion, they are well-designed.
class Questionnaire(TimeStampedModel):
    id = models.CharField(max_length=20, unique=True, verbose_name=_(" آیدی - شناسه یکتا"), primary_key=True)
    name = models.CharField(max_length=255, verbose_name=_("عنوان"))
    questions = models.ManyToManyField(
        Question, through="QuestionnaireQuestion", verbose_name=_("سوالات")
    )
    counter = models.IntegerField(default=0, verbose_name=_("Number of Questions"))
    class Meta:
        verbose_name = _("پرسشنامه")
        verbose_name_plural = _("پرسشنامه‌ها")

    def __str__(self):
        return f"{self.name!s}"

    # add a save def to count all the questions and add to the counter field
    def save(self, *args, **kwargs):
       
        super().save(*args, **kwargs)  # save first to saving the m to m 
        self.counter = self.questions.count()
        super().save(update_fields=["counter"])



class QuestionnaireQuestion(TimeStampedModel):
    questionnaire = models.ForeignKey(
        Questionnaire, on_delete=models.CASCADE, verbose_name=_("پرسشنامه")
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, verbose_name=_("سوال")
    )
    order = models.PositiveIntegerField(default=0, verbose_name=_("عدد ترتیب"))

    class Meta:
        verbose_name = _("سوال پرسشنامه")
        verbose_name_plural = _("سوالات پرسشنامه‌ها")
        constraints = [
            models.UniqueConstraint(
                fields=["questionnaire", "question"],
                name="unique_questionnaire_question",
            )
        ]
        ordering = ["order"]



class CompanyQuestionnaire(models.Model):
    company = models.ForeignKey(
        "company.CompanyProfile", on_delete=models.CASCADE, verbose_name=_("Company")
    )
    questionnaire = models.ForeignKey(
        "questionnaire.Questionnaire",
        on_delete=models.CASCADE,
        verbose_name=_("Questionnaire"),
    )
    question_counter = models.IntegerField(default=0)

    submitted_at = models.DateTimeField(
        auto_now_add=False, verbose_name=_("Submitted At"), null=True, blank=True
    )

    def __str__(self):
        return f"{self.company!s} - {self.questionnaire!s}"
    
    def save(self, *args, **kwargs):
        # Set question_counter based on the related questionnaire's counter
        self.question_counter = self.questionnaire.counter
        super().save(*args, **kwargs)  # Call the parent save method

    class Meta:
        verbose_name = _("Company Questionnaire")
        verbose_name_plural = _("Company Questionnaires")




class CompanyAnswer(models.Model):
    company_questionnaire = models.ForeignKey(
        "CompanyQuestionnaire",
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name=_("Company Questionnaire"),
    )
    question = models.ForeignKey(
        "questionnaire.Question", on_delete=models.CASCADE, verbose_name=_("Question")
    )
    selected_choice = models.ForeignKey(
        "questionnaire.QuestionChoice",
        on_delete=models.PROTECT,  # CHANGED: From SET_NULL to PROTECT for data safety
        null=True, # Still allow null if answer is not choice-based in the future
        blank=True,
        verbose_name=_("Selected Choice"),
    )
    answered_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Answered At"))

    def __str__(self):
        return f"{self.question!s}: {self.selected_choice!s}"

    class Meta:
        verbose_name = _("Company Answer")
        verbose_name_plural = _("Company Answers")
        # ADDED: Constraint to prevent duplicate answers for the same question.
        constraints = [
            models.UniqueConstraint(
                fields=["company_questionnaire", "question"],
                name="unique_company_answer_for_question",
            )
        ]