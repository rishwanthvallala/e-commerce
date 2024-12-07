from time import strftime
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from categories.models import Category
from utils.common_utils import generate_file_name


def product_image_directory_path(instance, filename):
    return 'products/{0}/{1}'.format(strftime('%Y/%m/%d'), generate_file_name() + '.' + filename.split('.')[-1])


STOCK_UNIT_CHOICES = (
    (1, 'kg'),
    (2, 'gm'),
    (3, 'ltr'),
    (4, 'ml'),
    (5, 'unit'),
)


class Product(TimeStampedModel):
    name = models.CharField(max_length=255, verbose_name=_("Product name"))
    description = models.TextField()
    image = models.ImageField(upload_to=product_image_directory_path)
    fake_price = models.IntegerField()
    sell_price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    brand = models.CharField(max_length=200, null=True, blank=True)
    weight = models.CharField(max_length=40, null=True, blank=True)
    stock = models.IntegerField()
    stock_unit = models.IntegerField(choices=STOCK_UNIT_CHOICES)
    top_featured = models.BooleanField(default=False)
    detail = models.TextField()
    detail_desc = models.TextField()

    quantity = models.IntegerField()
    quantity_unit = models.IntegerField(choices=STOCK_UNIT_CHOICES)
    discount_price = models.IntegerField()
    original_price = models.IntegerField()

    def __str__(self):
        return self.name
