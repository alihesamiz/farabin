from django.contrib import admin

from apps.swot.models import SWOTAnalysis, SWOTMatrix, SWOTOption, SWOTQuestion


@admin.register(SWOTAnalysis)
class SWOTAnalysisAdmin(admin.ModelAdmin):
    """Admin View for SWOTAnalysis"""

    list_display = ("matrix",)


@admin.register(SWOTOption)
class SWOTOptionAdmin(admin.ModelAdmin): ...


@admin.register(SWOTQuestion)
class SWOTQuestionAdmin(admin.ModelAdmin): ...


@admin.register(SWOTMatrix)
class SWOTModelMatrixAdmin(admin.ModelAdmin):
    """Admin View for SWOTModelMatrix"""

    list_display = ("company",)
