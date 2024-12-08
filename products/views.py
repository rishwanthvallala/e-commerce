from django.http import Http404
from django.views.generic import ListView, DetailView
from django.db.models import Q

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get similar products from the same category
        similar_products = Product.objects.filter(
            category=self.object.category,
            is_active=True
        ).exclude(
            id=self.object.id
        )[:6]
        
        # Get related products (from all categories)
        related_products = Product.objects.filter(
            is_active=True
        ).exclude(
            id=self.object.id
        ).exclude(
            id__in=[p.id for p in similar_products]
        )[:8]  # Limit to 8 products
        
        context['similar_products'] = similar_products
        context['related_products'] = related_products
        return context


class ProductsByCategoryView(ListView):
    model = Product
    template_name = "products/category.html"
    context_object_name = "products"

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs["slug"])
        if category:
            return Product.objects.filter(category=category)
        return Product.objects.none()
