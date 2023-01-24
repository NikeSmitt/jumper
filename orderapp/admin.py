from django.contrib import admin

from orderapp.models import Order, OrderItem


class OrderItemTabularInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    # readonly_fields = ('product', 'quantity')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemTabularInline, ]
    list_display = ['created_at', 'phone', 'comment']
    search_fields = ['phone']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'order']
    