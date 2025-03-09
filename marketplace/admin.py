from django.contrib import admin
from django.utils.html import format_html
from .models import Cart, CartItem, Order, OrderItem, Transaction

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    fields = ('product', 'quantity', 'unit_price', 'subtotal')
    readonly_fields = ('subtotal',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'item_count', 'total', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    inlines = [CartItemInline]
    readonly_fields = ('created_at', 'updated_at')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'quantity', 'unit_price', 'unit', 'subtotal', 'farmer')
    can_delete = False

class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 0
    readonly_fields = ('created_at', 'updated_at')
    fields = ('status', 'amount', 'payment_method', 'transaction_id', 'notes', 'created_at', 'updated_at')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number',
        'user',
        'total_amount',
        'status',
        'payment_method',
        'created_at',
        'order_status_badge'
    )
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = (
        'order_number',
        'user__username',
        'user__email',
        'shipping_address',
        'shipping_city'
    )
    readonly_fields = ('order_number', 'created_at', 'updated_at')
    inlines = [OrderItemInline, TransactionInline]
    fieldsets = (
        ('Informacione Bazë', {
            'fields': (
                'order_number',
                'user',
                'status',
                'total_amount',
                'payment_method'
            )
        }),
        ('Informacione Dërgese', {
            'fields': (
                'shipping_address',
                'shipping_city',
                'shipping_phone'
            )
        }),
        ('Detaje Shtesë', {
            'fields': (
                'notes',
                'created_at',
                'updated_at'
            )
        }),
    )

    def order_status_badge(self, obj):
        status_colors = {
            'pending': 'warning',
            'confirmed': 'info',
            'processing': 'primary',
            'shipping': 'secondary',
            'delivered': 'success',
            'cancelled': 'danger'
        }
        return format_html(
            '<span class="badge badge-{}">{}</span>',
            status_colors.get(obj.status, 'secondary'),
            obj.get_status_display()
        )
    order_status_badge.short_description = 'Statusi'

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'transaction_id',
        'order',
        'amount',
        'status',
        'payment_method',
        'created_at'
    )
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = (
        'transaction_id',
        'order__order_number',
        'order__user__username',
        'order__user__email'
    )
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Informacione Transaksioni', {
            'fields': (
                'order',
                'amount',
                'status',
                'transaction_id',
                'payment_method'
            )
        }),
        ('Detaje Shtesë', {
            'fields': (
                'notes',
                'created_at',
                'updated_at'
            )
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Nëse po përditësojmë një transaksion ekzistues
            return self.readonly_fields + ('order', 'amount', 'payment_method')
        return self.readonly_fields

# Regjistrimi i modeleve të tjera nëse nevojiten
admin.site.register(CartItem)
admin.site.register(OrderItem)
