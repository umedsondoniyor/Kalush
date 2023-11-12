from django.contrib import admin
from .models import ShoppingCart, Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'price', 'order_status', 'payment_status', 'created_at']
    list_filter = ['created_at', 'order_status', 'payment_status']
    list_editable = ['order_status', ]
    list_per_page = 50
    ordering = ['-created_at']
    search_fields = ['user']


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoice_no', 'item', 'image', 'quantity', 'price', 'total', 'created_at']
    list_filter = ['created_at']
    list_per_page = 50
    ordering = ['-created_at']
    search_fields = ['order']


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)





















