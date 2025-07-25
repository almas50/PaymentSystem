from django.contrib import admin
from .models import Item, OrderItem, Order, Discount, Tax


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ['id', 'created_at', 'discount', 'tax', 'total_amount_display']
    readonly_fields = ['total_amount_display']

    def total_amount_display(self, obj):
        return f"{obj.total_amount():.2f}"
    total_amount_display.short_description = "Total Amount"


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'item', 'quantity']


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'percent', 'currency']


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ['name', 'percent', 'currency']