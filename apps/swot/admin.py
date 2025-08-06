from django.contrib import admin

from apps.swot.models import (
    CompanySWOTOption,
    CompanySWOTOptionAnalysis,
    CompanySWOTOptionMatrix,
    CompanySWOTQuestion,
    CompanySWOTQuestionAnalysis,
    CompanySWOTQuestionMatrix,
    SWOTOption,
    SWOTQuestion,
)


@admin.register(SWOTOption)
class SWOTOptionAdmin(admin.ModelAdmin): ...


@admin.register(SWOTQuestion)
class SWOTQuestionAdmin(admin.ModelAdmin): ...


@admin.register(CompanySWOTQuestionAnalysis)
class SWOTQuestionAnalysisAdmin(admin.ModelAdmin): ...


@admin.register(CompanySWOTOptionAnalysis)
class SWOTOptionAnalysisAdmin(admin.ModelAdmin): ...


@admin.register(CompanySWOTOption)
class CompanySWOTOptionAdmin(admin.ModelAdmin): ...


@admin.register(CompanySWOTQuestion)
class CompanySWOTQuestionAdmin(admin.ModelAdmin): ...


@admin.register(CompanySWOTQuestionMatrix)
class CompanySWOTQuestionMatrixAdmin(admin.ModelAdmin): ...


@admin.register(CompanySWOTOptionMatrix)
class CompanySWOTOptionMatrixAdmin(admin.ModelAdmin): ...
