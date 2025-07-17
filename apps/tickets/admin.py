import nested_admin


from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import Count
from django.contrib import admin


from apps.tickets.models import Ticket, Agent, TicketAnswer, Attachment


class AttachmentInline(admin.StackedInline):
    model = Attachment
    extra = 0
    min_num = 0


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = [
        "issuer",
    ]


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = [
        "file",
        "created_at",
    ]


@admin.register(TicketAnswer)
class TicketAnswerAdmin(admin.ModelAdmin):
    list_display = [
        "issuer",
        "ticket",
        "description",
    ]


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ["agent"]
