from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import models


from core.utils import GeneralUtils


User = get_user_model()



class TicketAnswer(models.Model):

    ticket = models.ForeignKey(
        'Ticket', on_delete=models.CASCADE, verbose_name=_("Ticket"), related_name='answers')
    agent = models.ForeignKey(
        'Agent', on_delete=models.CASCADE, verbose_name=_("Agent"))

    comment = models.TextField(verbose_name=_("Comment"))

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Created At"))

    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Ticket Answer")
        verbose_name_plural = _("Ticket Answers")


class TicketComment(models.Model):

    ticket = models.ForeignKey(
        'Ticket', on_delete=models.CASCADE, verbose_name=_("Ticket"), related_name='comments')

    comment = models.TextField(verbose_name=_("Comment"))

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Created At"))

    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Ticket Comment")
        verbose_name_plural = _("Ticket Comments")


class Ticket(models.Model):

    ATTACHMENT_FILE_PATH = GeneralUtils(
        path="ticket_attachments",
        fields=['service', 'created_at'])

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

    issuer = models.ForeignKey(
        'company.CompanyProfile', on_delete=models.SET_NULL, null=True, verbose_name=_("Issuer"))

    subject = models.CharField(max_length=255, verbose_name=_("Subject"))

    comment = models.TextField(verbose_name=_("Comment"))

    service = models.ForeignKey(
        'core.Service', on_delete=models.CASCADE, verbose_name=_("Service"))
    department = models.ForeignKey(
        'Department', on_delete=models.CASCADE, verbose_name=_("Department"))
    status = models.CharField(max_length=255, verbose_name=_(
        "Status"), choices=STATUS_CHOICES, default=STATUS_NEW)
    priority = models.CharField(max_length=255, verbose_name=_(
        "Priority"), choices=PRIORITY_CHOICES)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Updated At"))

    def __str__(self):
        return f"{self.subject} : {self.priority}"

    class Meta:
        ordering = ['-updated_at']
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

    first_name = models.CharField(max_length=255, verbose_name=_(
        "First Name"), null=True, blank=True)

    last_name = models.CharField(max_length=255, verbose_name=_(
        "Last Name"), null=True, blank=True)

    email = models.EmailField(verbose_name=_("Email"), null=True, blank=True)

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name=_("User"))

    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="agents", verbose_name=_("Department"))

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = _("Agent")
        verbose_name_plural = _("Agents")