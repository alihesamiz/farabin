from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeStampedModel
from apps.core.utils import GeneralUtils
from constants.validators import Validator as _validator

User = get_user_model()


class Ticket(TimeStampedModel):
    class ServiceName(models.TextChoices):
        FINANCIAL = "financial", _("Financial")
        MANAGEMENT = "management", _("Management")
        MIS = "mis", _("MIS")
        RAD = "rad", _("R&D")
        MARKETING = "marketing", _("Marketing")
        PRODUCTION = "production", _("Production")

    class TicketStatus(models.TextChoices):
        NEW = "new", _("New")
        OPEN = "open", _("Open")
        IN_PROGRESS = "ip", _("In Progress")
        RESOLVED = "resolved", _("Resolved")
        CLOSED = "closed", _("Closed")

    class TicketPriority(models.TextChoices):
        LOW = "low", _("Low")
        MEDIUM = "med", _("Medium")
        HIGH = "high", _("High")
        CRITICAL = "crit", _("Critical")

    issuer = models.ForeignKey(
        "company.CompanyUser",
        on_delete=models.CASCADE,
        related_name="tickets",
        verbose_name=_("Issuer"),
    )
    title = models.CharField(
        max_length=100,
        verbose_name=_("Title"),
    )
    description = models.TextField(
        verbose_name=_("Description"),
    )
    service = models.CharField(
        max_length=10,
        choices=ServiceName.choices,
        verbose_name=_("Service"),
    )
    status = models.CharField(
        max_length=8,
        choices=TicketStatus.choices,
        default=TicketStatus.NEW,
        verbose_name=_("Status"),
    )
    priority = models.CharField(
        max_length=4,
        choices=TicketPriority.choices,
        default=TicketPriority.LOW,
        verbose_name=_("Priority"),
    )
    attachments = GenericRelation("Attachment")

    def __str__(self):
        return f"{self.issuer.company}({self.priority}): {self.title}"

    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")


class TicketReply(TimeStampedModel):
    issuer = models.ForeignKey(
        "company.CompanyUser",
        on_delete=models.CASCADE,
        related_name="ticket_replies",
        verbose_name=_("Issuer"),
    )
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="replies",
        verbose_name=_("Ticket"),
    )
    description = models.TextField(
        verbose_name=_("Description"),
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="child_replies",
    )
    attachments = GenericRelation("Attachment")

    def __str__(self):
        if self.parent:
            return f"Reply by {self.issuer} to Reply({self.parent.id})"
        return f"Reply by {self.issuer} to Ticket({self.ticket.pk})"

    class Meta:
        verbose_name = _("Ticket Reply")
        verbose_name_plural = _("Ticket Replies")


def get_ticket_attachment_file_upload_path(instance, filename):
    path = GeneralUtils(
        path="tickets_attachements", fields=["ticket__service"]
    ).rename_folder(instance, filename)
    return path


class Attachment(TimeStampedModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    file = models.FileField(
        upload_to="tickets/",
        null=True,
        blank=True,
        verbose_name=_("File"),
        validators=[_validator.ticket_file_validator],
    )

    def __str__(self):
        return f"Attachment for {self.content_object}"


class Agent(TimeStampedModel):
    agent = models.OneToOneField(
        User,
        verbose_name=_("Agent"),
        on_delete=models.CASCADE,
        related_name="agents",
    )

    def __str__(self):
        return f"{self.agent.first_name} {self.agent.last_name}"

    class Meta:
        verbose_name = _("Agent")
        verbose_name_plural = _("Agents")


class TicketAnswer(TimeStampedModel):
    issuer = models.ForeignKey(
        Agent,
        on_delete=models.CASCADE,
        related_name="tickets",
        verbose_name=_("Issuer"),
    )
    ticket = models.ForeignKey(
        Ticket,
        verbose_name=_("Ticket"),
        on_delete=models.CASCADE,
        related_name=_("answers"),
    )
    description = models.TextField(
        verbose_name=_("Description"),
    )
    attachments = GenericRelation("Attachment")

    def __str__(self):
        return f"{self.issuer.agent.first_name} {self.issuer.agent.last_name}"

    class Meta:
        verbose_name = _("Ticket Answer")
        verbose_name_plural = _("Ticket Answers")
