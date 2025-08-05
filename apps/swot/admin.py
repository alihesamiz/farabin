from django.contrib import admin

from apps.swot.models import (
    CompanySWOTOption,
    CompanySWOTOptionMatrix,
    CompanySWOTQuestion,
    CompanySWOTQuestionMatrix,
    SWOTOption,
    SWOTQuestion,
    SWOTQuestionAnalysis,
)


@admin.register(SWOTOption)
class SWOTOptionAdmin(admin.ModelAdmin): ...


@admin.register(SWOTQuestion)
class SWOTQuestionAdmin(admin.ModelAdmin): ...


@admin.register(SWOTQuestionAnalysis)
class SWOTQuestionAnalysisAdmin(admin.ModelAdmin): ...


@admin.register(CompanySWOTOption)
class CompanySWOTOptionAdmin(admin.ModelAdmin): ...


@admin.register(CompanySWOTQuestion)
class CompanySWOTQuestionAdmin(admin.ModelAdmin): ...


@admin.register(CompanySWOTQuestionMatrix)
class CompanySWOTQuestionMatrixAdmin(admin.ModelAdmin): ...


@admin.register(CompanySWOTOptionMatrix)
class CompanySWOTOptionMatrixAdmin(admin.ModelAdmin): ...
