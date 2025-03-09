from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

class FarmLocation(models.Model):
    """Model për vendndodhjen e fermës"""
    address = models.CharField(_('Adresa'), max_length=255)
    address_en = models.CharField(_('Address'), max_length=255, null=True, blank=True)
    address_sq = models.CharField(_('Adresa'), max_length=255, null=True, blank=True)
    city = models.CharField(_('Qyteti'), max_length=100)
    city_en = models.CharField(_('City'), max_length=100, null=True, blank=True)
    city_sq = models.CharField(_('Qyteti'), max_length=100, null=True, blank=True)
    region = models.CharField(_('Rajoni'), max_length=100)
    region_en = models.CharField(_('Region'), max_length=100, null=True, blank=True)
    region_sq = models.CharField(_('Rajoni'), max_length=100, null=True, blank=True)
    country = models.CharField(_('Shteti'), max_length=100, default='Shqipëri')
    country_en = models.CharField(_('Country'), max_length=100, default='Albania', null=True, blank=True)
    country_sq = models.CharField(_('Shteti'), max_length=100, default='Shqipëri', null=True, blank=True)
    latitude = models.DecimalField(
        _('Gjerësia gjeografike'),
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )
    longitude = models.DecimalField(
        _('Gjatësia gjeografike'),
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _('Vendndodhja e Fermës')
        verbose_name_plural = _('Vendndodhjet e Fermave')

    def __str__(self):
        return f"{self.address}, {self.city}, {self.country}"

class CultivationMethod(models.Model):
    """Model për metodat e kultivimit"""
    name = models.CharField(_('Emri'), max_length=100)
    description = models.TextField(_('Përshkrimi'))

    name_en = models.CharField(_('Name'), max_length=100, null=True, blank=True)
    name_sq = models.CharField(_('Emri'), max_length=100, null=True, blank=True)
    description = models.TextField(_('Përshkrimi'))
    description_en = models.TextField(_('Description'), null=True, blank=True)
    description_sq = models.TextField(_('Përshkrimi'), null=True, blank=True)

    class Meta:
        verbose_name = _('Metoda e Kultivimit')
        verbose_name_plural = _('Metodat e Kultivimit')

    def __str__(self):
        return self.name

class Certification(models.Model):
    """Model për certifikimet e fermerit"""
    name = models.CharField(_('Emri'), max_length=100)
    name_en = models.CharField(_('Name'), max_length=100, null=True, blank=True)
    name_sq = models.CharField(_('Emri'), max_length=100, null=True, blank=True)
    issuing_organization = models.CharField(_('Organizata lëshuese'), max_length=200)
    issuing_organization_en = models.CharField(_('Issuing Organization'), max_length=200, null=True, blank=True)
    issuing_organization_sq = models.CharField(_('Organizata lëshuese'), max_length=200, null=True, blank=True)
    issue_date = models.DateField(_('Data e lëshimit'))
    expiry_date = models.DateField(_('Data e skadimit'))
    document = models.FileField(_('Dokumenti'), upload_to='certifications/')
    
    class Meta:
        verbose_name = _('Certifikim')
        verbose_name_plural = _('Certifikimet')

    def __str__(self):
        return f"{self.name} ({self.issuing_organization})"

class Crop(models.Model):
    """Model për kulturat bujqësore"""
    name = models.CharField(_('Emri'), max_length=100)
    scientific_name = models.CharField(_('Emri shkencor'), max_length=200, blank=True, null=True)
    name_en = models.CharField(_('Name'), max_length=100, null=True, blank=True)
    name_sq = models.CharField(_('Emri'), max_length=100, null=True, blank=True)
    scientific_name = models.CharField(_('Emri shkencor'), max_length=200, blank=True, null=True)
    scientific_name_en = models.CharField(_('Scientific Name'), max_length=200, blank=True, null=True)
    scientific_name_sq = models.CharField(_('Emri shkencor'), max_length=200, blank=True, null=True)
    description = models.TextField(_('Përshkrimi'), blank=True)
    description_en = models.TextField(_('Description'), blank=True, null=True)
    description_sq = models.TextField(_('Përshkrimi'), blank=True, null=True)
    growing_season = models.CharField(_('Sezoni i rritjes'), max_length=100, blank=True)
    growing_season_en = models.CharField(_('Growing Season'), max_length=100, blank=True, null=True)
    growing_season_sq = models.CharField(_('Sezoni i rritjes'), max_length=100, blank=True, null=True)
    image = models.ImageField(_('Imazhi'), upload_to='crops/', blank=True, null=True)

    class Meta:
        verbose_name = _('Kulturë Bujqësore')
        verbose_name_plural = _('Kulturat Bujqësore')

    def __str__(self):
        return self.name

class FarmerProfile(models.Model):
    """Profili i zgjeruar i fermerit"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='farmer_profile'
    )
    farm_name = models.CharField(_('Emri i fermës'), max_length=200)
    farm_name_en = models.CharField(_('Farm Name'), max_length=200, null=True, blank=True)
    farm_name_sq = models.CharField(_('Emri i fermës'), max_length=200, null=True, blank=True)
    farm_description = models.TextField(_('Përshkrimi i fermës'), blank=True)
    farm_description_en = models.TextField(_('Farm Description'), blank=True, null=True)
    farm_description_sq = models.TextField(_('Përshkrimi i fermës'), blank=True, null=True)
    profile_image = models.ImageField(
        _('Imazhi i profilit'),
        upload_to='farmer_profiles/',
        blank=True,
        null=True
    )
    phone_number = models.CharField(_('Numri i telefonit'), max_length=20, blank=True)
    website = models.URLField(_('Faqja e internetit'), blank=True)
    year_established = models.PositiveIntegerField(
        _('Viti i themelimit'),
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(2100)
        ],
        blank=True,
        null=True
    )

    # Lidhjet me modelet e tjera
    location = models.ForeignKey(
        FarmLocation,
        on_delete=models.SET_NULL,
        null=True,
        related_name='farmers'
    )
    cultivation_methods = models.ManyToManyField(
        CultivationMethod,
        related_name='farmers'
    )
    certifications = models.ManyToManyField(
        Certification,
        related_name='farmers',
        blank=True
    )

    # Fushat shtesë
    total_land_area = models.DecimalField(
        _('Sipërfaqja totale e tokës (ha)'),
        max_digits=10,
        decimal_places=2,
        default=0
    )
    is_verified = models.BooleanField(_('I verifikuar'), default=False)
    is_active = models.BooleanField(_('Aktiv'), default=True)
    registration_date = models.DateTimeField(_('Data e regjistrimit'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Përditësuar më'), auto_now=True)

    class Meta:
        verbose_name = _('Profili i Fermerit')
        verbose_name_plural = _('Profilet e Fermerëve')

    def __str__(self):
        return f"{self.farm_name} ({self.user.get_full_name() or self.user.username})"

    @property
    def full_address(self):
        if self.location:
            return str(self.location)
        return None

class FarmerCrop(models.Model):
    """Lidhja midis fermerit dhe kulturave që kultivon"""
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    land_area = models.DecimalField(
        _('Sipërfaqja e tokës (ha)'),
        max_digits=8,
        decimal_places=2
    )
    cultivation_method = models.ForeignKey(
        CultivationMethod,
        on_delete=models.SET_NULL,
        null=True
    )
    estimated_yield = models.DecimalField(
        _('Rendimenti i përllogaritur (kg/ha)'),
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _('Kultura e Fermerit')
        verbose_name_plural = _('Kulturat e Fermerit')
        unique_together = ('farmer', 'crop')

    def __str__(self):
        return f"{self.crop.name} - {self.farmer.farm_name}"

class ProductionLog(models.Model):
    """Dokumentimi i procesit të prodhimit"""
    ACTIVITY_CHOICES = [
        ('planting', _('Mbjellje')),
        ('fertilizing', _('Plehërim')),
        ('irrigating', _('Ujitje')),
        ('pest_control', _('Kontroll i dëmtuesve')),
        ('harvesting', _('Vjelje')),
        ('other', _('Tjetër')),
    ]

    farmer = models.ForeignKey(
        FarmerProfile,
        on_delete=models.CASCADE,
        related_name='production_logs'
    )
    crop = models.ForeignKey(
        Crop,
        on_delete=models.CASCADE,
        related_name='production_logs'
    )
    activity_type = models.CharField(
        _('Lloji i aktivitetit'),
        max_length=20,
        choices=ACTIVITY_CHOICES
    )
    activity_type_en = models.CharField(_('Activity Type'), max_length=20, choices=ACTIVITY_CHOICES, null=True, blank=True)
    activity_type_sq = models.CharField(_('Lloji i aktivitetit'), max_length=20, choices=ACTIVITY_CHOICES, null=True, blank=True)
    date = models.DateField(_('Data'))
    description = models.TextField(_('Përshkrimi'))
    description_en = models.TextField(_('Description'), null=True, blank=True)
    description_sq = models.TextField(_('Përshkrimi'), null=True, blank=True)
    photo = models.ImageField(
        _('Foto'),
        upload_to='production_logs/',
        blank=True,
        null=True
    )
    notes = models.TextField(_('Shënime'), blank=True)
    notes_en = models.TextField(_('Notes'), blank=True, null=True)
    notes_sq = models.TextField(_('Shënime'), blank=True, null=True)
    created_at = models.DateTimeField(_('Krijuar më'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Përditësuar më'), auto_now=True)

    # Të dhënat për gjurmim
    blockchain_hash = models.CharField(
        _('Hash Blockchain'),
        max_length=255,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _('Regjistri i Prodhimit')
        verbose_name_plural = _('Regjistrat e Prodhimit')
        ordering = ['-date']

    def __str__(self):
        return f"{self.get_activity_type_display()} - {self.crop.name} - {self.date}"
