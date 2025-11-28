from django.contrib import admin
from .models import *

admin.site.register(Supplier)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(SupplierOrder)
admin.site.register(SupplierOrderItem)
admin.site.register(Stock)
admin.site.register(Shipment)
admin.site.register(ShipmentItem)
admin.site.register(Invoice)
