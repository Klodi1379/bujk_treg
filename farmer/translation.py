from modeltranslation.translator import register, TranslationOptions
from .models import FarmLocation, CultivationMethod, Certification, Crop, FarmerProfile, ProductionLog

@register(FarmLocation)
class FarmLocationTranslationOptions(TranslationOptions):
    fields = ('address', 'city', 'region', 'country',)

@register(CultivationMethod)
class CultivationMethodTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)

@register(Certification)
class CertificationTranslationOptions(TranslationOptions):
    fields = ('name', 'issuing_organization',)

@register(Crop)
class CropTranslationOptions(TranslationOptions):
    fields = ('name', 'scientific_name', 'description', 'growing_season',)

@register(FarmerProfile)
class FarmerProfileTranslationOptions(TranslationOptions):
    fields = ('farm_name', 'farm_description',)

@register(ProductionLog)
class ProductionLogTranslationOptions(TranslationOptions):
    fields = ('description', 'notes',)
