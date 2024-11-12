from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from .models import Ticket, Department, Agent, TicketAnswer, TicketComment
import nested_admin
# Register your models here.


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'population']

    @admin.display(description=_('Members count'))
    def population(self, department: Department):
        return department.agents.count()
    population.short_description = _('Members count')


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']
    list_display = ['user', 'department']


class TicketCommentInline(nested_admin.NestedTabularInline):
    model = TicketComment
    fields = ('comment', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    extra = 0


class TicketAnswerInline(nested_admin.NestedTabularInline):
    model = TicketAnswer
    fields = ('agent', 'comment', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    extra = 0
    inlines = [TicketCommentInline]


@admin.register(Ticket)
class TicketAdmin(nested_admin.NestedModelAdmin):
    list_display = ['company_title', 'subject', 'department', 'status',
                    'priority', 'created_at', 'updated_at']
    search_fields = ('subject', 'description', 'department__name')
    list_filter = ('status', 'priority', 'department')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [TicketAnswerInline]

    def company_title(self, ticket: Ticket):
        return f"{ticket.issuer.company_title}"
    company_title.short_description = _('Company Title')

    # def get_queryset(self, request):
    #     # Limit queryset based on the user's department if needed
    #     qs = super().get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs  # Superuser can see all tickets
    #     try:
    #         agent = Agent.objects.get(user=request.user)
    #         # Filter by agent's department
    #         return qs.filter(department=agent.department)
    #     except Agent.DoesNotExist:
    #         return qs.none()
