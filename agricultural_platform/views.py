from django.shortcuts import render
from django.views.generic import TemplateView
from product.models import Product

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_products'] = Product.objects.filter(availability='in_stock').order_by('-created_at')[:3]
        return context
