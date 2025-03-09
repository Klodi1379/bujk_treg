from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from product.models import Product
from farmer.models import FarmerProfile

class Cart(models.Model):
    """Modeli për shportën e blerjes"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Përdoruesi'),
        on_delete=models.CASCADE,
        related_name='carts',
        null=True, # Allow null for guest users
        blank=True # Allow blank for guest users
    )
    created_at = models.DateTimeField(_('Krijuar më'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Përditësuar më'), auto_now=True)

    class Meta:
        verbose_name = _('Shportë')
        verbose_name_plural = _('Shportat')

    def __str__(self):
        return f"Shporta e {self.user.get_full_name() or self.user.username}"

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())

    @property
    def item_count(self):
        return self.items.count()

class CartItem(models.Model):
    """Modeli për produktet në shportë"""
    cart = models.ForeignKey(
        Cart,
        verbose_name=_('Shporta'),
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        verbose_name=_('Produkti'),
        on_delete=models.CASCADE
    )
    quantity = models.DecimalField(
        _('Sasia'),
        max_digits=10,
        decimal_places=2
    )
    unit_price = models.DecimalField(
        _('Çmimi për njësi'),
        max_digits=10,
        decimal_places=2
    )
    added_at = models.DateTimeField(_('Shtuar më'), auto_now_add=True)

    class Meta:
        verbose_name = _('Produkt në shportë')
        verbose_name_plural = _('Produktet në shportë')
        unique_together = ['cart', 'product']

    def __str__(self):
        return f"{self.quantity} {self.product.get_unit_display()} {self.product.name}"

    @property
    def subtotal(self):
        return self.quantity * self.unit_price

class Order(models.Model):
    """Modeli për porositë"""
    STATUS_CHOICES = [
        ('pending', _('Në pritje')),
        ('confirmed', _('Konfirmuar')),
        ('processing', _('Në përpunim')),
        ('shipping', _('Në transport')),
        ('delivered', _('Dorëzuar')),
        ('cancelled', _('Anuluar')),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('cash', _('Para në dorë')),
        ('bank_transfer', _('Transfertë bankare')),
        ('card', _('Kartë krediti/debiti')),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Blerësi'),
        on_delete=models.SET_NULL,
        null=True,  # Make user field optional
        blank=True,
        related_name='orders'
    )
    order_number = models.CharField(
        _('Numri i porosisë'),
        max_length=20,
        unique=True
    )
    status = models.CharField(
        _('Statusi'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    total_amount = models.DecimalField(
        _('Shuma totale'),
        max_digits=10,
        decimal_places=2
    )
    payment_method = models.CharField(
        _('Metoda e pagesës'),
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES
    )
    shipping_address = models.TextField(_('Adresa e dorëzimit'))
    shipping_address_en = models.TextField(_('Shipping Address'), null=True, blank=True)
    shipping_address_sq = models.TextField(_('Adresa e dorëzimit'), null=True, blank=True)
    shipping_city = models.CharField(_('Qyteti'), max_length=100)
    shipping_city_en = models.CharField(_('City'), max_length=100, null=True, blank=True)
    shipping_city_sq = models.CharField(_('Qyteti'), max_length=100, null=True, blank=True)
    shipping_phone = models.CharField(_('Telefoni'), max_length=20)
    notes = models.TextField(_('Shënime'), blank=True)
    notes_en = models.TextField(_('Notes'), blank=True, null=True)
    notes_sq = models.TextField(_('Shënime'), blank=True, null=True)
    created_at = models.DateTimeField(_('Krijuar më'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Përditësuar më'), auto_now=True)

    class Meta:
        verbose_name = _('Porosi')
        verbose_name_plural = _('Porositë')
        ordering = ['-created_at']

    def __str__(self):
        return f"Porosi #{self.order_number}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            last_order = Order.objects.order_by('-id').first()
            if last_order:
                last_number = int(last_order.order_number[3:])
                self.order_number = f"ORD{last_number + 1:06d}"
            else:
                self.order_number = "ORD000001"
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    """Modeli për produktet në porosi"""
    order = models.ForeignKey(
        Order,
        verbose_name=_('Porosia'),
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        verbose_name=_('Produkti'),
        on_delete=models.SET_NULL,
        null=True
    )
    farmer = models.ForeignKey(
        FarmerProfile,
        verbose_name=_('Fermeri'),
        on_delete=models.SET_NULL,
        null=True
    )
    product_name = models.CharField(_('Emri i produktit'), max_length=200)
    product_name_en = models.CharField(_('Product Name'), max_length=200, null=True, blank=True)
    product_name_sq = models.CharField(_('Emri i produktit'), max_length=200, null=True, blank=True)
    quantity = models.DecimalField(
        _('Sasia'),
        max_digits=10,
        decimal_places=2
    )
    unit_price = models.DecimalField(
        _('Çmimi për njësi'),
        max_digits=10,
        decimal_places=2
    )
    unit = models.CharField(_('Njësia'), max_length=10)
    subtotal = models.DecimalField(
        _('Nëntotali'),
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        verbose_name = _('Produkt i porosisë')
        verbose_name_plural = _('Produktet e porosisë')

    def __str__(self):
        return f"{self.quantity} {self.unit} {self.product_name}"

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)

class Transaction(models.Model):
    """Modeli për transaksionet"""
    STATUS_CHOICES = [
        ('pending', _('Në pritje')),
        ('completed', _('Kompletuar')),
        ('failed', _('Dështuar')),
        ('refunded', _('Rimbursuar')),
    ]

    order = models.ForeignKey(
        Order,
        verbose_name=_('Porosia'),
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    amount = models.DecimalField(
        _('Shuma'),
        max_digits=10,
        decimal_places=2
    )
    status = models.CharField(
        _('Statusi'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    transaction_id = models.CharField(
        _('ID e transaksionit'),
        max_length=100,
        unique=True,
        blank=True,
        null=True
    )
    payment_method = models.CharField(
        _('Metoda e pagesës'),
        max_length=20,
        choices=Order.PAYMENT_METHOD_CHOICES
    )
    created_at = models.DateTimeField(_('Krijuar më'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Përditësuar më'), auto_now=True)
    notes = models.TextField(_('Shënime'), blank=True)
    notes_en = models.TextField(_('Notes'), blank=True, null=True)
    notes_sq = models.TextField(_('Shënime'), blank=True, null=True)

    class Meta:
        verbose_name = _('Transaksion')
        verbose_name_plural = _('Transaksionet')
        ordering = ['-created_at']

    def __str__(self):
        return f"Transaksion {self.transaction_id or 'N/A'} për Porosinë #{self.order.order_number}"
