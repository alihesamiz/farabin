from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.
User = get_user_model()


class Ticket(models.Model):

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_RESOLVED = 'resolved'
    STATUS_CLOSED = 'closed'

    STATUS_CHOICES = [
        (STATUS_NEW, _('New')),
        (STATUS_IN_PROGRESS, _('In Progress')),
        (STATUS_RESOLVED, _('Resolved')),
        (STATUS_CLOSED, _('Closed')),
    ]

    PRIORITY_LOW = 'low'
    PRIORITY_MEDIUM = 'medium'
    PRIORITY_HIGH = 'high'

    PRIORITY_CHOICES = [
        (PRIORITY_LOW, _('Low')),
        (PRIORITY_MEDIUM, _('Medium')),
        (PRIORITY_HIGH, _('High')),]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("Customer"))
    subject = models.CharField(max_length=255, verbose_name=_("Subject"))
    description = models.TextField(verbose_name=_("Description"))
    department = models.ForeignKey(
        'Department', on_delete=models.CASCADE, verbose_name=_("Department"))
    status = models.CharField(max_length=255, verbose_name=_(
        "Status"), choices=STATUS_CHOICES)
    priority = models.CharField(max_length=255, verbose_name=_(
        "Priority"), choices=PRIORITY_CHOICES)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Updated At"))

    def __str__(self):
        return f"{self.subject} - {self.customer} : {self.priority}"

    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")


class Department(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    description = models.TextField(verbose_name=_("Description"))

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = _("Department")
        verbose_name_plural = _("Departments")


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="agents")

    def __str__(self):
        return f"{self.user}"
