from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from farmer.models import FarmerProfile, Crop

class Category(models.Model):
    """Model për kategoritë e produkteve"""
    name = models.CharField(_('Emri'), max_length=100)
    name_en = models.CharField(_('Name'), max_length=100, null=True, blank=True)
    name_sq = models.CharField(_('Emri'), max_length=100, null=True, blank=True)
    slug = models.SlugField(_('Slug'), unique=True)
    description = models.TextField(_('Përshkrimi'), blank=True)
    description_en = models.TextField(_('Description'), blank=True, null=True)
    description_sq = models.TextField(_('Përshkrimi'), blank=True, null=True)
    parent = models.ForeignKey(
        'self',
        verbose_name=_('Kategoria prind'),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    image = models.ImageField(
        _('Imazhi'),
        upload_to='categories/',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _('Kategori')
        verbose_name_plural = _('Kategoritë')
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/produktet/kategoria/{self.slug}/"

class Product(models.Model):
    """Model për produktet bujqësore"""
    UNIT_CHOICES = [
        ('kg', 'Kilogram'),
        ('g', 'Gram'),
        ('piece', 'Copë'),
        ('box', 'Kuti'),
        ('bunch', 'Tufë'),
    ]

    AVAILABILITY_CHOICES = [
        ('in_stock', _('Në gjendje')),
        ('out_of_stock', _('Nuk ka në gjendje')),
        ('coming_soon', _('Së shpejti')),
        ('pre_order', _('Para-porosi')),
    ]

    name = models.CharField(_('Emri'), max_length=200)
    slug = models.SlugField(_('Slug'), unique=True)
    farmer = models.ForeignKey(
        FarmerProfile,
        verbose_name=_('Fermeri'),
        on_delete=models.CASCADE,
        related_name='products'
    )
    category = models.ForeignKey(
        Category,
        verbose_name=_('Kategoria'),
        on_delete=models.SET_NULL,
        null=True,
        related_name='products'
    )
    crop = models.ForeignKey(
        Crop,
        verbose_name=_('Kultura'),
        on_delete=models.SET_NULL,
        null=True,
        related_name='products'
    )
    name = models.CharField(_('Emri'), max_length=200)
    name_en = models.CharField(_('Name'), max_length=200, null=True, blank=True)
    name_sq = models.CharField(_('Emri'), max_length=200, null=True, blank=True)
    description = models.TextField(_('Përshkrimi'))
    description_en = models.TextField(_('Description'), null=True, blank=True)
    description_sq = models.TextField(_('Përshkrimi'), null=True, blank=True)
    price = models.DecimalField(
        _('Çmimi'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    discount_price = models.DecimalField(
        _('Çmimi me ulje'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    unit = models.CharField(
        _('Njësia'),
        max_length=10,
        choices=UNIT_CHOICES,
        default='kg'
    )
    minimum_order = models.DecimalField(
        _('Sasia minimale e porosisë'),
        max_digits=10,
        decimal_places=2,
        default=1,
        validators=[MinValueValidator(0.1)]
    )
    stock = models.DecimalField(
        _('Sasia në gjendje'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    availability = models.CharField(
        _('Disponueshmëria'),
        max_length=20,
        choices=AVAILABILITY_CHOICES,
        default='in_stock'
    )
    is_organic = models.BooleanField(_('Organik'), default=False)
    is_featured = models.BooleanField(_('I veçantë'), default=False)
    harvest_date = models.DateField(_('Data e vjeljes'), null=True, blank=True)
    expiry_date = models.DateField(_('Data e skadencës'), null=True, blank=True)
    created_at = models.DateTimeField(_('Krijuar më'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Përditësuar më'), auto_now=True)

    class Meta:
        verbose_name = _('Produkt')
        verbose_name_plural = _('Produktet')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['slug']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.name} ({self.farmer.farm_name})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/produktet/{self.slug}/"

    @property
    def discount_percentage(self):
        if self.discount_price and self.price:
            return int((1 - self.discount_price / self.price) * 100)
        return 0

    @property
    def is_in_stock(self):
        return self.stock > 0 and self.availability == 'in_stock'

class ProductImage(models.Model):
    """Model për imazhet e produkteve"""
    product = models.ForeignKey(
        Product,
        verbose_name=_('Produkti'),
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(_('Imazhi'), upload_to='products/')
    is_primary = models.BooleanField(_('Imazh kryesor'), default=False)
    alt_text = models.CharField(
        _('Teksti alternativ'),
        max_length=200,
        blank=True
    )
    alt_text_en = models.CharField(_('Alternative Text'), max_length=200, blank=True, null=True)
    alt_text_sq = models.CharField(_('Teksti alternativ'), max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(_('Krijuar më'), auto_now_add=True)

    class Meta:
        verbose_name = _('Imazh i Produktit')
        verbose_name_plural = _('Imazhet e Produkteve')
        ordering = ['-is_primary', 'created_at']

    def __str__(self):
        return f"Imazh për {self.product.name}"

    def save(self, *args, **kwargs):
        if self.is_primary:
            # Sigurohu që vetëm një imazh të jetë primar
            ProductImage.objects.filter(
                product=self.product,
                is_primary=True
            ).exclude(id=self.id).update(is_primary=False)
        super().save(*args, **kwargs)

class Review(models.Model):
    """Model për vlerësimet e produkteve"""
    product = models.ForeignKey(
        Product,
        verbose_name=_('Produkti'),
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(
        'auth.User',
        verbose_name=_('Përdoruesi'),
        on_delete=models.CASCADE,
        related_name='product_reviews'
    )
    rating = models.IntegerField(
        _('Vlerësimi'),
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(_('Komenti'))
    created_at = models.DateTimeField(_('Krijuar më'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Përditësuar më'), auto_now=True)
    is_verified = models.BooleanField(
        _('I verifikuar'),
        default=False,
        help_text=_('Tregon nëse vlerësimi është nga një blerës i verifikuar')
    )
    comment = models.TextField(_('Komenti'))
    comment_en = models.TextField(_('Comment'), null=True, blank=True)
    comment_sq = models.TextField(_('Komenti'), null=True, blank=True)

    class Meta:
        verbose_name = _('Vlerësim')
        verbose_name_plural = _('Vlerësimet')
        ordering = ['-created_at']
        unique_together = ['product', 'user']  # Një përdorues mund të vlerësojë një produkt vetëm një herë

    def __str__(self):
        return f"Vlerësim nga {self.user.get_full_name() or self.user.username} për {self.product.name}"

class ProductQuestion(models.Model):
    """Model për pyetjet rreth produkteve"""
    product = models.ForeignKey(
        Product,
        verbose_name=_('Produkti'),
        on_delete=models.CASCADE,
        related_name='questions'
    )
    user = models.ForeignKey(
        'auth.User',
        verbose_name=_('Pyetësi'),
        on_delete=models.CASCADE,
        related_name='product_questions'
    )
    question = models.TextField(_('Pyetja'))
    answer = models.TextField(_('Përgjigja'), blank=True, null=True)
    answered_by = models.ForeignKey(
        'auth.User',
        verbose_name=_('Përgjigjur nga'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='product_answers'
    )
    asked_at = models.DateTimeField(_('Pyetur më'), auto_now_add=True)
    answered_at = models.DateTimeField(_('Përgjigjur më'), null=True, blank=True)
    is_public = models.BooleanField(
        _('Publike'),
        default=True,
        help_text=_('Tregon nëse pyetja është e dukshme për të gjithë')
    )
    question = models.TextField(_('Pyetja'))
    question_en = models.TextField(_('Question'), null=True, blank=True)
    question_sq = models.TextField(_('Pyetja'), null=True, blank=True)
    answer = models.TextField(_('Përgjigja'), blank=True, null=True)
    answer_en = models.TextField(_('Answer'), blank=True, null=True)
    answer_sq = models.TextField(_('Përgjigja'), blank=True, null=True)

    class Meta:
        verbose_name = _('Pyetje për Produktin')
        verbose_name_plural = _('Pyetjet për Produktet')
        ordering = ['-asked_at']

    def __str__(self):
        return f"Pyetje nga {self.user.get_full_name() or self.user.username} për {self.product.name}"
