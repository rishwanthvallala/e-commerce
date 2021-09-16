from time import strftime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.common_utils import generate_file_name


def image_directory_path(instance, filename):
    return 'categories/{0}/{1}'.format(strftime('%Y/%m/%d'), generate_file_name() + '.' + filename.split('.')[-1])


class Category(models.Model):
    name = models.CharField(max_length=250, verbose_name=_("Name"))
    slug = models.SlugField(unique=True, verbose_name=_("Slug"))
    image = models.ImageField(upload_to=image_directory_path, verbose_name=_("Image"))

    def __str__(self):
        return self.name
