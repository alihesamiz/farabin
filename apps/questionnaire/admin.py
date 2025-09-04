from django.contrib import admin

from apps.questionnaire.models import (
    CompanyAnswer,
    CompanyQuestionnaire,
    Question,
    QuestionChoice,
    QuestionMetric,
    Questionnaire,
    QuestionnaireQuestion,
)

# --- Question and related components ---


@admin.register(CompanyAnswer)
class CompanyAnswerAdmin(admin.ModelAdmin):
    list_display = ["question", "selected_choice"]


class QuestionChoiceInline(admin.TabularInline):
    """
    Allows editing Choices directly within the Question admin page.
    """

    model = QuestionChoice
    extra = 1  # Start with one empty choice form


# ADDED: An inline for managing Metrics directly within the Question admin page.
class QuestionMetricInline(admin.TabularInline):
    """
    Allows editing Metrics directly within the Question admin page.
    """

    model = QuestionMetric
    extra = 0  # Metrics might not always be needed, so start with none.


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "created_at")
    search_fields = ("text",)
    # CHANGED: Added QuestionMetricInline to manage all related objects in one place.
    inlines = [QuestionChoiceInline, QuestionMetricInline]


# --- Questionnaire and its linking table ---


class QuestionnaireQuestionInline(admin.TabularInline):
    """
    Manages the relationship between a Questionnaire and its Questions.
    """

    model = QuestionnaireQuestion
    extra = 1
    # Use autocomplete_fields for better performance with many questions.
    autocomplete_fields = ["question"]
    ordering = ["order"]


@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('id', "name", "question_count", "created_at", "updated_at")
    search_fields = ("name",)
    inlines = [QuestionnaireQuestionInline]

    # ADDED: A calculated field to show how many questions are in a questionnaire.
    @admin.display(description="Number of Questions")
    def question_count(self, obj):
        return obj.questions.count()


# --- Company Submissions and Answers ---


# ADDED: A read-only inline to VIEW answers within a company's submission.
class CompanyAnswerInline(admin.TabularInline):
    """
    Displays the answers submitted for a CompanyQuestionnaire.
    This is configured to be read-only as answers should be submitted via the API,
    and this view is for administrative review.
    """

    model = CompanyAnswer
    extra = 0

    # Fields to display in the inline table
    fields = ("question", "selected_choice", "answered_at")
    readonly_fields = ("question", "selected_choice", "answered_at")

    # Use autocomplete for better display of foreign keys
    autocomplete_fields = ("question", "selected_choice")

    # Prevent adding, changing, or deleting answers from the admin interface.
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(CompanyQuestionnaire)
class CompanyQuestionnaireAdmin(admin.ModelAdmin):
    list_display = ("company", "questionnaire", "submitted_at")
    list_filter = ("questionnaire", "submitted_at")
    search_fields = ("company__name", "questionnaire__name")
    readonly_fields = ("submitted_at",)
    # ADDED: A date hierarchy for easy filtering by submission date.
    date_hierarchy = "submitted_at"
    # ADDED: The inline to review submitted answers directly on this page.
    inlines = [CompanyAnswerInline]


# --- Standalone Model Admins (Optional but good for data overview) ---


@admin.register(QuestionChoice)
class QuestionChoiceAdmin(admin.ModelAdmin):
    """
    Admin for viewing all choices across all questions.
    """

    list_display = ("answer", "question", "points")
    list_filter = ("question__text",)
    search_fields = ("answer", "question__text")
    autocomplete_fields = ["question"]


# The following registrations are no longer necessary as they are managed via inlines,
# but can be kept if you want a top-level view of ALL metrics or ALL answers.
# For a cleaner admin, it's better to remove them.

# admin.site.register(QuestionMetric)
# admin.site.register(CompanyAnswer)
