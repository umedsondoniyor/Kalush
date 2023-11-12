from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe

from Product.models import ProductVariant
from Profile.models import Address


status_choices = (
    ('process', 'Processing'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
    ('process', 'Processing'),
)


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(ProductVariant)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Shopping Cart - User: {self.user}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_status = models.CharField(max_length=100)
    order_status = models.CharField(choices=status_choices, max_length=30, default='processing')
    created_at = models.DateTimeField(auto_now_add=True)

    items = models.ManyToManyField('OrderItem', related_name='items_in_order')
    billing_address = models.ForeignKey(Address, related_name='billing_orders', on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(Address, related_name='shipping_orders', on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order - User: {self.user}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    product_status = models.CharField(max_length=200, default='')
    item = models.CharField(max_length=200, null=True, blank=True)
    image = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    invoice_no = models.CharField(max_length=200, null=True, blank=True)

    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order Item - Product: {self.product_variant} - Quantity: {self.quantity}"

    def order_img(self):
        return mark_safe('<img src="/media/%s" width="50" height="50"/>' % self.image)

