# @receiver(post_save, sender=Order)
# def create_subscription_of_confirmed_order(sender: Order, instance: Order, *args, **kwargs):
#     if instance.status == Order.OrderStatus.PAID_STATUS:
#         with atomic():

#             subscription, created = Subscription.objects.get_or_create(
#                 user=instance.user,
#             )
#             subscription.package = instance.package

#             if not subscription.purchase_date:
#                 subscription.purchase_date = now()

#             if instance.service.exists():
#                 subscription.service.set(
#                     instance.service.all())

#                 [duration := subscription._calculate_duration(
#                     ser.period) for ser in subscription.service.all()]
#                 expires_at = subscription.purchase_date + duration
#                 Subscription.objects.filter(pk=subscription.pk).update(
#                     duration=duration, expires_at=expires_at)

#             Order.objects.filter(pk=instance.pk).update(
#                 status=Order.OrderStatus.CONFIRMED_STATUS)
