from products.models import Category
from core.models import SiteSettings


def common_data(request):
    categories = Category.objects.all().order_by("name").reverse()
    return {
        "categories": categories,
        "settings": SiteSettings.load()
    }
