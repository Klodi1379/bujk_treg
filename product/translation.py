from modeltranslation.translator import register, TranslationOptions
from .models import Category, Product, ProductImage, Review, ProductQuestion

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)

@register(ProductImage)
class ProductImageTranslationOptions(TranslationOptions):
    fields = ('alt_text',)

@register(Review)
class ReviewTranslationOptions(TranslationOptions):
    fields = ('comment',)

@register(ProductQuestion)
class ProductQuestionTranslationOptions(TranslationOptions):
    fields = ('question', 'answer',)
