from django.http import Http404
from django.views.generic import ListView, DetailView

from .models import Product
from categories.models import Category


class ProductListView(ListView):
    model = Product
    template_name = "products/index.html"
    context_object_name = "products"
    paginate_by = 10


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/detail.html"
    context_object_name = "product"
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj is None:
            raise Http404("Product not found")
        return obj


class ProductsByCategoryView(ListView):
    model = Product
    template_name = "products/category.html"
    context_object_name = "products"

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs["slug"])
        if category:
            return Product.objects.filter(category=category)
        return Product.objects.none()
