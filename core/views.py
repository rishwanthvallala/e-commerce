from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Exists, OuterRef
from django.db import models

from products.models import Product
from wishlist.models import Wishlist


def index(request):
    products = Product.objects.all()

    if request.user.is_authenticated:
        # Annotate products with wishlist status for the current user
        products = products.annotate(
            is_wishlisted=Exists(
                Wishlist.objects.filter(user=request.user, product=OuterRef("pk"))
            )
        )
    else:
        # For unauthenticated users, set is_wishlisted to False
        products = products.annotate(
            is_wishlisted=models.Value(False, output_field=models.BooleanField())
        )

    context = {
        "products": products,
    }
    return render(request, "index.html", context)

def search_view(request):
    if request.method == "POST":
        query = request.POST.get("query", "").strip()  # Get the search query from the form
        if query:
            # Perform a search on the relevant models (e.g., Product)
            results = Product.objects.filter(name__icontains=query)  # Adjust as needed
        else:
            results = []

        # Render the search results
        return render(request, 'search.html', {
            'query': query,
            'products': results,
        })
    else:
        # Redirect to home or an error page if accessed via GET
        return render(request, 'search.html')


class AboutView(TemplateView):
    template_name = "core/about.html"


class ContactView(TemplateView):
    template_name = "core/contact.html"


class TermsView(TemplateView):
    template_name = "core/terms.html"


class PrivacyView(TemplateView):
    template_name = "core/privacy.html"


class FAQView(TemplateView):
    template_name = "core/faq.html"


class RefundView(TemplateView):
    template_name = "core/refund.html"

def hello(request):
    # return string hello
    return render(request, 'hello.html')