from django.db import models
from products.models import Product, ProductVariant
from decimal import Decimal
from django.core.exceptions import ValidationError
from django_extensions.db.models import TimeStampedModel

from users.models import User


class Cart(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())

    def get_total(self):
        return self.total_price + Decimal("50.00")


class CartItem(TimeStampedModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(
        ProductVariant, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        # Use variant price if variant exists, otherwise use product price
        unit_price = self.variant.selling_price if self.variant else self.product.selling_price
        return unit_price * self.quantity

    def __str__(self):
        variant_info = f" ({self.variant})" if self.variant else ""
        return f"{self.product}{variant_info} x {self.quantity}"

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"

    @property
    def subtotal(self):
        if self.variant:
            return self.variant.selling_price * self.quantity
        return self.product.selling_price * self.quantity

    def clean(self):
        if self.quantity > self.product.stock:
            raise ValidationError("Requested quantity exceeds available stock")
