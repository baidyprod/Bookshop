from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import BookItem, Order, OrderItem, OrderItemBookItem


@receiver(post_save, sender=OrderItem)
def create_order_item_book_items(sender, instance, created, **kwargs):
    if created:
        quantity = instance.quantity

        for _ in range(quantity):
            OrderItemBookItem.objects.create(
                order=instance.order,
                order_item=instance,
                book_item=None
            )


@receiver(post_save, sender=Order)
def delete_book_items(sender, instance, created, **kwargs):
    if instance.status == Order.SUCCESS and instance.pk:
        order_items = OrderItem.objects.filter(order=instance)
        order_item_book_items = OrderItemBookItem.objects.filter(order_item__in=order_items)
        book_item_pks = order_item_book_items.values_list('book_item__pk', flat=True).distinct()
        BookItem.objects.filter(pk__in=book_item_pks).delete()
