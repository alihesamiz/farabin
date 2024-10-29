from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.dispatch import receiver
from .models import Ticket

@receiver(post_save, sender=Ticket)
def notify_agent_on_ticket_creation(sender, instance, created, **kwargs):
    if created:
        agent = instance.agent
        if agent:
            send_mail(
                subject="New Ticket Assigned",
                message=f"A new ticket (ID: {instance.id} ) for user {instance.user} has been assigned to you.",
                from_email="support@example.com",
                recipient_list=[agent.user.email],
            )
