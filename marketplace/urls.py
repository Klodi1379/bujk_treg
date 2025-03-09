from django.urls import path
from django.urls import path
from . import views
from django.conf.urls.i18n import i18n_patterns

app_name = 'marketplace'

from . import views

app_name = 'marketplace'

urlpatterns = [
    # Cart URLs
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add/<slug:slug>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    
    # Order URLs
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders/create/', views.create_order, name='create_order'),
    
    # Checkout URLs
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('checkout/confirm/', views.confirm_order, name='confirm_order'),
    path('checkout/success/<int:pk>/', views.OrderSuccessView.as_view(), name='order_success'),
    
    # Seller Dashboard URLs
    path('seller/dashboard/', views.SellerDashboardView.as_view(), name='seller_dashboard'),
    path('seller/orders/', views.SellerOrderListView.as_view(), name='seller_orders'),
    path('seller/orders/<int:pk>/', views.SellerOrderDetailView.as_view(), name='seller_order_detail'),
    path('seller/orders/<int:pk>/update/', views.update_order_status, name='update_order_status'),
    
    # API Endpoints
    path('api/cart/count/', views.get_cart_count, name='get_cart_count'),
    path('api/cart/total/', views.get_cart_total, name='get_cart_total'),
    path('api/check-stock/<slug:slug>/', views.check_product_stock, name='check_stock'),
    
    # Cancel Order URL
    path('orders/<int:pk>/cancel/', views.cancel_order, name='cancel_order'),
]
