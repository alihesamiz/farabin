from django.contrib import admin

from apps.swot.models import (
    SWOTModelMatrix,
    SWOTOption,
    SWOTQuestion,
)


@admin.register(SWOTOption)
class SWOTOptionAdmin(admin.ModelAdmin): ...


@admin.register(SWOTQuestion)
class SWOTQuestionAdmin(admin.ModelAdmin): ...


@admin.register(SWOTModelMatrix)
class SWOTModelMatrixAdmin(admin.ModelAdmin):
    """Admin View for SWOTModelMatrix"""

    list_display = ("company",)
