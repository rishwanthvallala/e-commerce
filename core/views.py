from django.shortcuts import render
from django.views.generic import TemplateView

from categories.models import Category
from products.models import Product

def index(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'index.html', context)


class AboutView(TemplateView):
    template_name = 'core/about.html'


class ContactView(TemplateView):
    template_name = 'core/contact.html'


class TermsView(TemplateView):
    template_name = 'core/terms.html'


class PrivacyView(TemplateView):
    template_name = 'core/privacy.html'


class FAQView(TemplateView):
    template_name = 'core/faq.html'


class RefundView(TemplateView):
    template_name = 'core/refund.html'
