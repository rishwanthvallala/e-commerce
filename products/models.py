from time import strftime
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from categories.models import Category
from utils.common_utils import generate_file_name


def product_image_directory_path(instance, filename):
    return "products/{0}/{1}".format(
        strftime("%Y/%m/%d"), generate_file_name() + "." + filename.split(".")[-1]
    )


class Product(TimeStampedModel):
    class StockUnitChoices(models.IntegerChoices):
        KG = 1, "kg"
        GM = 2, "gm"
        LTR = 3, "ltr"
        ML = 4, "ml"
        UNIT = 5, "unit"

    name = models.CharField(max_length=255, verbose_name=_("Product name"))
    description = models.TextField(help_text=_("Main product description"))

    # Price fields using DecimalField
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    brand = models.CharField(max_length=200, null=True, blank=True)
    weight = models.CharField(max_length=40, null=True, blank=True)

    stock = models.IntegerField()
    stock_unit = models.IntegerField(choices=StockUnitChoices.choices)

    quantity = models.IntegerField()
    quantity_unit = models.IntegerField(choices=StockUnitChoices.choices)

    top_featured = models.BooleanField(default=False)
    additional_details = models.TextField(blank=True)

    class Meta:
        ordering = ["-created"]
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.name

    @property
    def discount_percentage(self):
        """Calculate discount percentage"""
        if self.original_price and self.selling_price:
            discount = (
                (self.original_price - self.selling_price) / self.original_price
            ) * 100
            return round(discount, 2)
        return 0

    @property
    def primary_image(self):
        """Returns the primary image or the first image if no primary is set"""
        return (
            self.images.filter(is_primary=True).first() or 
            self.images.first()
        )


class ProductImage(TimeStampedModel):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(
        upload_to=product_image_directory_path,
        verbose_name=_("Product Image")
    )
    is_primary = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")

    def __str__(self):
        return f"Image for {self.product.name}"
