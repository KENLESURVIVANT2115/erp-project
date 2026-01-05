from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

from .models import (
    SupplierOrderItem,
    ShipmentItem,
    Stock
)



@receiver(post_save, sender=SupplierOrderItem)
def increase_stock_after_supplier_order(sender, instance, created, **kwargs):
    if not created:
        return

    stock, _ = Stock.objects.get_or_create(product=instance.product)
    stock.quantity += instance.quantity
    stock.save()


@receiver(post_save, sender=ShipmentItem)
def decrease_stock_after_shipment(sender, instance, created, **kwargs):
    if not created:
        return

    stock, _ = Stock.objects.get_or_create(product=instance.product)

    if stock.quantity < instance.quantity:
        raise ValidationError(
            f"Not enough stock for product {instance.product.name}"
        )

    stock.quantity -= instance.quantity
    stock.save()
