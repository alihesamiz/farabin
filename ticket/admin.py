from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from .models import Ticket, Department, Agent
# Register your models here.


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['user', 'department', 'priority',
                    'status', 'created_at', 'updated_at']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'population']

    @admin.display(description=_('Members count'))
    def population(self, department: Department):
        return department.agents.count()
    population.short_description = _('Members count')


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ['user', 'department']
