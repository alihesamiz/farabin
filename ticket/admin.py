from .models import Ticket, TicketAnswer, Agent, TicketDescription
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from .models import Ticket, Department, Agent, TicketAnswer
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


class TicketAnswerInline(admin.TabularInline):
    model = TicketAnswer
    fields = ('agent', 'comment', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    extra = 1  # Number of empty forms to display for adding new answers


class TicketDescriptionInline(admin.TabularInline):
    model = TicketDescription
    fields = ('comment', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    extra = 1  # Number of empty forms to display for adding new descriptions


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('subject', 'department', 'status',
                    'priority', 'created_at', 'updated_at')
    search_fields = ('subject', 'description', 'department__name')
    list_filter = ('status', 'priority', 'department')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [TicketDescriptionInline, TicketAnswerInline, ]

    def get_queryset(self, request):
        # Limit queryset based on the user's department if needed
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Superuser can see all tickets
        try:
            agent = Agent.objects.get(user=request.user)
            # Filter by agent's department
            return qs.filter(department=agent.department)
        except Agent.DoesNotExist:
            return qs.none()
