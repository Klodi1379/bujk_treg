from django.contrib import admin
from django.utils.html import format_html
from .models import (
    FarmLocation,
    CultivationMethod,
    Certification,
    Crop,
    FarmerProfile,
    FarmerCrop,
    ProductionLog
)

@admin.register(FarmLocation)
class FarmLocationAdmin(admin.ModelAdmin):
    list_display = ('address', 'city', 'region', 'country')
    search_fields = ('address', 'city', 'region')
    list_filter = ('region', 'city')

@admin.register(CultivationMethod)
class CultivationMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'issuing_organization', 'issue_date', 'expiry_date', 'document_link')
    search_fields = ('name', 'issuing_organization')
    list_filter = ('issuing_organization', 'issue_date')

    def document_link(self, obj):
        if obj.document:
            return format_html('<a href="{}" target="_blank">Shiko dokumentin</a>', obj.document.url)
        return '-'
    document_link.short_description = 'Dokumenti'

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('name', 'scientific_name', 'growing_season', 'crop_image')
    search_fields = ('name', 'scientific_name')
    list_filter = ('growing_season',)

    def crop_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return '-'
    crop_image.short_description = 'Imazhi'

class FarmerCropInline(admin.TabularInline):
    model = FarmerCrop
    extra = 1

@admin.register(FarmerProfile)
class FarmerProfileAdmin(admin.ModelAdmin):
    list_display = ('farm_name', 'user', 'phone_number', 'total_land_area', 'is_verified', 'is_active')
    list_filter = ('is_verified', 'is_active', 'registration_date')
    search_fields = ('farm_name', 'user__username', 'user__email', 'phone_number')
    inlines = [FarmerCropInline]
    readonly_fields = ('registration_date', 'last_modified')
    fieldsets = (
        ('Informacione Bazë', {
            'fields': (
                'user', 'farm_name', 'farm_description', 'profile_image',
                'phone_number', 'website', 'year_established'
            )
        }),
        ('Vendndodhja dhe Metodat', {
            'fields': (
                'location', 'cultivation_methods', 'certifications'
            )
        }),
        ('Të dhëna shtesë', {
            'fields': (
                'total_land_area', 'is_verified', 'is_active',
                'registration_date', 'last_modified'
            )
        }),
    )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)

@admin.register(FarmerCrop)
class FarmerCropAdmin(admin.ModelAdmin):
    list_display = ('farmer', 'crop', 'land_area', 'cultivation_method', 'estimated_yield')
    list_filter = ('farmer', 'crop', 'cultivation_method')
    search_fields = ('farmer__farm_name', 'crop__name')

@admin.register(ProductionLog)
class ProductionLogAdmin(admin.ModelAdmin):
    list_display = ('activity_type', 'farmer', 'crop', 'date', 'has_photo', 'created_at')
    list_filter = ('activity_type', 'date', 'farmer', 'crop')
    search_fields = ('farmer__farm_name', 'crop__name', 'description')
    date_hierarchy = 'date'
    readonly_fields = ('created_at', 'updated_at', 'blockchain_hash')

    def has_photo(self, obj):
        return bool(obj.photo)
    has_photo.boolean = True
    has_photo.short_description = 'Ka foto'

    fieldsets = (
        ('Informacione Bazë', {
            'fields': (
                'farmer', 'crop', 'activity_type', 'date',
                'description', 'photo'
            )
        }),
        ('Informacione Shtesë', {
            'fields': (
                'notes', 'blockchain_hash',
                'created_at', 'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )
