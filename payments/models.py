from django.db import models
from django.core.exceptions import ValidationError


class Discount(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, default="usd")

    def clean(self):
        if not self.amount and not self.percent:
            raise ValidationError('Должен быть указан amount или percent')
        if self.amount and self.percent:
            raise ValidationError('Должен быть указан amount или percent')

    def __str__(self):
        if self.percent:
            return f"{self.name} ({self.percent}%)"
        else:
            return f"{self.name} ({self.amount} {self.currency})"

class Tax(models.Model):
    name = models.CharField(max_length=100)
    percent = models.DecimalField(max_digits=5, decimal_places=2)
    currency = models.CharField(max_length=3, default="usd")

    def __str__(self):
        return f"{self.name} ({self.percent}%)"

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField(Item, through="OrderItem")
    discount = models.ForeignKey(Discount, null=True, blank=True, on_delete=models.SET_NULL)
    tax = models.ForeignKey(Tax, null=True, blank=True, on_delete=models.SET_NULL)

    def total_amount(self):
        subtotal = sum(oi.total_price() for oi in self.orderitem_set.all())
        discount_amount = 0
        if self.discount:
            if self.discount.percent:
                discount_amount = subtotal * (self.discount.percent / 100)
            else:
                discount_amount = float(self.discount.amount)
        taxed_amount = subtotal - discount_amount
        if self.tax:
            tax_amount = taxed_amount * (self.tax.percent / 100)
        else:
            tax_amount = 0
        return max(taxed_amount + tax_amount, 0)

    def __str__(self):
        return f"Order #{self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.item.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"
