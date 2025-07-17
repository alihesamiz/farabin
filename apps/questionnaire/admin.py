from django.contrib import admin

from apps.questionnaire.models import QuestionMetric, Question, QuestionChoice, Questionnaire, QuestionnaireQuestion


class QuestionChoiceInline(admin.TabularInline):
    model = QuestionChoice
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "created_at")
    search_fields = ("text",)
    inlines = [QuestionChoiceInline]


class QuestionnaireQuestionInline(admin.TabularInline):
    model = QuestionnaireQuestion
    extra = 1
    autocomplete_fields = ['question']


@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)
    inlines = [QuestionnaireQuestionInline]


@admin.register(QuestionChoice)
class QuestionChoiceAdmin(admin.ModelAdmin):
    list_display = ("question", "answer", "points")
    list_filter = ("question",)
    search_fields = ("answer",)


@admin.register(QuestionMetric)
class QuestionMetricAdmin(admin.ModelAdmin):
    list_display = ["question", "title", "created_at"]
