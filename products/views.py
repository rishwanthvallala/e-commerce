from django.http import Http404
from django.views.generic import ListView, DetailView
from django.db.models import Q

from .models import Product
from categories.models import Category


class ProductListView(ListView):
    model = Product
    template_name = "products/all.html"
    context_object_name = "products"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "All Products"
        return context


class FeaturedProductListView(ListView):
    model = Product
    template_name = "products/all.html"
    context_object_name = "products"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Featured Products"
        return context


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
            category=self.object.category, is_active=True
        ).exclude(id=self.object.id)[:6]

        # Get related products (from all categories)
        related_products = (
            Product.objects.filter(is_active=True)
            .exclude(id=self.object.id)
            .exclude(id__in=[p.id for p in similar_products])[:8]
        )  # Limit to 8 products

        context["similar_products"] = similar_products
        context["related_products"] = related_products
        return context


class ProductsByCategoryView(ListView):
    model = Product
    template_name = "products/all.html"
    context_object_name = "products"
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        self.get_category()
        return super().dispatch(request, *args, **kwargs)

    def get_category(self):
        self.category = Category.objects.get(slug=self.kwargs["slug"])
        if self.category is None:
            raise Http404("Category not found")
        return self.category

    def get_queryset(self):
        if self.category:
            return Product.objects.filter(category=self.category)
        return Product.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"List of {self.category.name} Products"
        return context
