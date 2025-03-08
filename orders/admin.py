from django.contrib import admin

# Register your models here.
from orders.models import Item, Order, ItemQuantity


class ItemQuantityInline(admin.TabularInline):
    model = ItemQuantity
    extra = 1


class ItemAdmin(admin.ModelAdmin):
    inlines = [ItemQuantityInline]
    list_display = ["name", "price"]
    search_fields = ["name"]
    list_filter = ["name"]
    list_display_links = ["name"]


class OrderAdmin(admin.ModelAdmin):
    inlines = [ItemQuantityInline]
    list_display = ["id", "status", "table_number", "total_price"]
    search_fields = ["id", "status", "created_at", "items"]
    list_filter = ["id", "status", "created_at", "items"]
    list_display_links = ["id"]


admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ItemQuantity)
