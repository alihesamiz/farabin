from django.db.models.signals import post_save
from django.db.transaction import atomic
from django.dispatch import receiver


from packages.models import Order, Subscription


@receiver(post_save, sender=Order)
def create_subscription_of_paied_order(sender: Order, instance: Order, *args, **kwargs):
    if instance.status == Order.OrderStatus.CONFIRMED_STATUS:
        with atomic():
            subscription, created = Subscription.objects.get_or_create(
                user=instance.user, package=instance.package)
