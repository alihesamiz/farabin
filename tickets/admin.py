import nested_admin



from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import Count
from django.contrib import admin


from tickets.models import Ticket, Department, Agent, TicketAnswer, TicketComment


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_agents_count']

    @admin.display(description=_('Members count'))
    def get_agents_count(self, department: Department):
        """Return the number of agents in the department."""
        return department.agents.count()
    get_agents_count.short_description = _('Members count')

    class AgentInline(nested_admin.NestedStackedInline):
        model = Agent
        extra = 0 
        fields = ['first_name', 'last_name', 'email',
                  'user']  

    inlines = [AgentInline]


    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        return queryset.annotate(agent_count=Count('agents'))

    class Meta:
        verbose_name = _("Department")
        verbose_name_plural = _("Departments")


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):

    list_display = ['first_name', 'last_name',
                    'phone_number', 'email', 'department']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if db_field.name == "user":
            group = Group.objects.get(name='Editor')

            kwargs['queryset'] = get_user_model().objects.filter(
                is_staff=True, groups=group)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    @admin.display(ordering='user__phone_number')
    def phone_number(self, agent: Agent):
        return agent.user.phone_number
    phone_number.short_description = _('Phone Number')


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



@admin.register(Ticket)
class TicketAdmin(nested_admin.NestedModelAdmin):
    list_display = ['company_title', 'subject', 'department', 'status',
                    'priority', 'created_at', 'updated_at']
    search_fields = ('subject', 'description', 'department__name')
    list_filter = ('status', 'priority', 'department')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    inlines = [TicketAnswerInline,TicketCommentInline]

    def company_title(self, ticket: Ticket):
        return f"{ticket.issuer.company_title}"
    company_title.short_description = _('Company Title')

    def get_queryset(self, request):
        
        qs = super().get_queryset(request)

        
        if request.user.is_superuser:
            return qs

        
        try:
            agent = Agent.objects.get(user=request.user)
            return qs.filter(department=agent.department)
        except Agent.DoesNotExist:
            
            return qs.none()

    def save_formset(self, request, form, formset, change):
        """
        Override save_formset to set the agent for TicketAnswer automatically.
        """
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, TicketAnswer) and not instance.agent_id:
                try:

                    instance.agent = Agent.objects.get(user=request.user)
                except Agent.DoesNotExist:

                    raise ValueError("Only agents can respond to tickets.")
            instance.save()
        formset.save_m2m()
