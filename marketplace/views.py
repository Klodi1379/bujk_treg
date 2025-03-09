from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, View
from django.db.models import Sum
from django.http import JsonResponse
from django.utils import timezone
from django.urls import reverse
from product.models import Product
from .models import Cart, CartItem, Order, OrderItem, Transaction
from .forms import (
    AddToCartForm,
    UpdateCartItemForm,
    CheckoutForm,
    UpdateOrderStatusForm,
    PaymentForm
)

class CartView(LoginRequiredMixin, View):
    """Pamja e shportës së blerjeve"""
    template_name = 'marketplace/cart.html'

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        return render(request, self.template_name, {'cart': cart})

@login_required
def add_to_cart(request, slug):
    """Shto produkt në shportë"""
    product = get_object_or_404(Product, slug=slug)
    cart, created = Cart.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = AddToCartForm(request.POST, product=product)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            
            # Kontrollo disponueshmërinë
            if quantity > product.stock:
                messages.error(request, 'Sasia e kërkuar nuk është në dispozicion.')
                return redirect('product:detail', slug=slug)

            # Shto ose përditëso sasinë në shportë
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={
                    'quantity': quantity,
                    'unit_price': product.discount_price or product.price
                }
            )

            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            messages.success(request, 'Produkti u shtua në shportë.')
            return redirect('marketplace:cart')
    
    return redirect('product:detail', slug=slug)

@login_required
def update_cart_item(request, item_id):
    """Përditëso sasinë e produktit në shportë"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if request.method == 'POST':
        form = UpdateCartItemForm(request.POST, instance=cart_item)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            
            # Kontrollo disponueshmërinë
            if quantity > cart_item.product.stock:
                messages.error(request, 'Sasia e kërkuar nuk është në dispozicion.')
            elif quantity < cart_item.product.minimum_order:
                messages.error(request, f'Sasia minimale është {cart_item.product.minimum_order}.')
            else:
                cart_item.quantity = quantity
                cart_item.save()
                messages.success(request, 'Sasia u përditësua.')

    return redirect('marketplace:cart')

@login_required
def remove_from_cart(request, item_id):
    """Hiq produkt nga shporta"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, 'Produkti u hoq nga shporta.')
    return redirect('marketplace:cart')

class CheckoutView(View):
    """Pamja e checkout-it"""
    template_name = 'marketplace/checkout.html'

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user) # Use get_or_create for cart
        if not cart.items.exists():
            messages.error(request, 'Shporta juaj është bosh.')
            return redirect('marketplace:cart')

        form = CheckoutForm()
        return render(request, self.template_name, {
            'cart': cart,
            'form': form
        })

    def post(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user) # Use get_or_create for cart
        form = CheckoutForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            else:
                # Guest user order details
                order.guest_name = form.cleaned_data['guest_name']
                order.guest_email = form.cleaned_data['guest_email']

            order.total_amount = cart.total
            order.save()

            # Create order items
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    farmer=item.product.farmer,
                    product_name=item.product.name,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    unit=item.product.unit,
                    subtotal=item.subtotal
                )

                # Update stock
                product = item.product
                product.stock -= item.quantity
                product.save()

            # Clear cart
            cart.items.all().delete()
            request.session['cart_id'] = None # Clear cart ID for guest users

            messages.success(request, 'Porosia u krijua me sukses.')
            return redirect('marketplace:order_success', pk=order.pk)
        else:
            messages.error(request, 'Gabim në formë. Ju lutem kontrolloni detajet e porosisë.')
            return render(request, self.template_name, {'cart': cart, 'form': form})


class OrderListView(LoginRequiredMixin, ListView):
    """Lista e porosive të përdoruesit"""
    model = Order
    template_name = 'marketplace/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

class OrderDetailView(LoginRequiredMixin, DetailView):
    """Detajet e porosisë"""
    model = Order
    template_name = 'marketplace/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class OrderSuccessView(LoginRequiredMixin, DetailView):
    """Pamja e suksesit të porosisë"""
    model = Order
    template_name = 'marketplace/order_success.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class SellerDashboardView(LoginRequiredMixin, View):
    """Paneli i shitësit"""
    template_name = 'marketplace/seller_dashboard.html'

    def get(self, request):
        if not hasattr(request.user, 'farmer_profile'):
            messages.error(request, 'Vetëm fermerët mund të aksesojnë këtë faqe.')
            return redirect('home')

        # Statistikat e shitjeve
        today = timezone.now().date()
        orders = OrderItem.objects.filter(
            farmer=request.user.farmer_profile,
            order__created_at__date=today
        )
        
        context = {
            'daily_sales': orders.aggregate(Sum('subtotal'))['subtotal__sum'] or 0,
            'daily_orders': orders.count(),
            'pending_orders': orders.filter(order__status='pending').count(),
            'recent_orders': orders.order_by('-order__created_at')[:5]
        }
        
        return render(request, self.template_name, context)

class SellerOrderListView(LoginRequiredMixin, ListView):
    """Lista e porosive për shitësin"""
    template_name = 'marketplace/seller_orders.html'
    context_object_name = 'orders'
    paginate_by = 20

    def get_queryset(self):
        return OrderItem.objects.filter(
            farmer=request.user.farmer_profile
        ).order_by('-order__created_at')

class SellerOrderDetailView(LoginRequiredMixin, DetailView):
    """Detajet e porosisë për shitësin"""
    template_name = 'marketplace/seller_order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.filter(
            items__farmer=self.request.user.farmer_profile
        ).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_form'] = UpdateOrderStatusForm(instance=self.object)
        return context

@login_required
def update_order_status(request, pk):
    """Përditëso statusin e porosisë"""
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = UpdateOrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Statusi u përditësua me sukses.')
        else:
            messages.error(request, 'Ndodhi një gabim gjatë përditësimit të statusit.')
    
    return redirect('marketplace:seller_order_detail', pk=pk)

@login_required
def create_order(request):
    """Pamja për krijimin e porosisë (placeholder)"""
    return render(request, 'marketplace/order_create.html') # Placeholder template

@login_required
def confirm_order(request):
    """Pamja për konfirmimin e porosisë (placeholder)"""
    return render(request, 'marketplace/order_confirm.html') # Placeholder template

# API Views
@login_required
def get_cart_count(request):
    """Merr numrin e produkteve në shportë"""
    cart = Cart.objects.filter(user=request.user).first()
    count = cart.items.count() if cart else 0
    return JsonResponse({'count': count})

@login_required
def get_cart_total(request):
    """Merr totalin e shportës"""
    cart = Cart.objects.filter(user=request.user).first()
    total = cart.total if cart else 0
    return JsonResponse({'total': total})

@login_required
@login_required
def cancel_order(request, pk):
    """Anulon një porosi."""
    order = get_object_or_404(Order, pk=pk, user=request.user)
    if order.status == 'pending':
        order.status = 'cancelled'
        order.save()
        messages.success(request, 'Porosia u anulua me sukses.')
    else:
        messages.error(request, 'Nuk mund të anuloni një porosi që nuk është në pritje.')
    return redirect('marketplace:order_detail', pk=pk)

def check_product_stock(request, slug):
    """Kontrollo disponueshmërinë e produktit"""
    product = get_object_or_404(Product, slug=slug)
    return JsonResponse({'in_stock': product.is_in_stock,
        'stock': product.stock,
        'minimum_order': product.minimum_order
    })
