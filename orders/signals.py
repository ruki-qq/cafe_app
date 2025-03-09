from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from orders.models import ItemQuantity


@receiver([post_save, post_delete], sender=ItemQuantity)
def update_order_items_price(sender, instance, **kwargs):
    """
    Высчитать total_price заказа когда ItemQuantity сохраняется или удаляется.
    """
    order = instance.order
    order.total_price = sum(
        item_quantity.item.price * item_quantity.quantity
        for item_quantity in order.itemquantity_set.all()
    )
    order.save()
