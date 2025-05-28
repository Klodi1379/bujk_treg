"""
Core context processors for global template variables.
"""
from django.conf import settings
from django.contrib.sites.models import Site


def site_context(request):
    """
    Add site-wide context variables to all templates.
    """
    context = {
        'site_name': 'Platforma Bujqësore',
        'site_description': 'Platforma moderne për fermerët dhe blerësit',
        'current_site': Site.objects.get_current() if hasattr(Site, 'objects') else None,
    }
    
    # Add cart item count for authenticated users
    if hasattr(request, 'user') and request.user.is_authenticated:
        try:
            from marketplace.models import Cart
            cart = Cart.objects.filter(user=request.user).first()
            context['cart_item_count'] = cart.item_count if cart else 0
        except:
            context['cart_item_count'] = 0
    else:
        context['cart_item_count'] = 0
    
    return context
