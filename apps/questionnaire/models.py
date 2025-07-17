from django.utils.translation import gettext_lazy as _
from django.db import models

from apps.core.models import TimeStampedModel


class QuestionMetric(TimeStampedModel):
    question = models.ForeignKey(
        "QuestionChoice", on_delete=models.CASCADE, related_name="metric", verbose_name=_("سوال"))
    title = models.CharField(verbose_name=_("Title"), max_length=128)
    weight = models.DecimalField(verbose_name=_(
        "Weight"), max_digits=4, decimal_places=2)

    class Meta:
        verbose_name = _("شاخص سوال")
        verbose_name_plural = _("شاخص‌های سوالات")

    def __str__(self):
        return f"{self.title!s}"


class QuestionChoice(models.Model):
    question = models.ForeignKey(
        "Question", on_delete=models.CASCADE, related_name="choices", verbose_name=_("سوال")
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


class Questionnaire(TimeStampedModel):
    name = models.CharField(max_length=255, verbose_name=_("عنوان"))
    questions = models.ManyToManyField(
        Question, through="QuestionnaireQuestion", verbose_name=_("سوالات")
    )

    class Meta:
        verbose_name = _("پرسشنامه")
        verbose_name_plural = _("پرسشنامه‌ها")

    def __str__(self):
        return f"{self.name!s}"


class QuestionnaireQuestion(TimeStampedModel):
    questionnaire = models.ForeignKey(
        Questionnaire, on_delete=models.CASCADE, verbose_name=_("پرسشنامه"))
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, verbose_name=_("سوال"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("عدد ترتیب"))

    class Meta:
        verbose_name = _("سوال پرسشنامه")
        verbose_name_plural = _("سوالات پرسشنامه‌ها")
        constraints = [
            models.UniqueConstraint(
                fields=["questionnaire", "question"],
                name="unique_questionnaire_question"
            )
        ]
        ordering = ['order']
