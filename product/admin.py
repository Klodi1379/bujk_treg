from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Avg
from .models import Category, Product, ProductImage, Review, ProductQuestion

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'product_count', 'show_image')
    list_filter = ('parent',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Numri i produkteve'
    
    def show_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return '-'
    show_image.short_description = 'Imazhi'

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'is_primary', 'alt_text')

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ('user', 'rating', 'comment', 'created_at')
    can_delete = False
    max_num = 0

class ProductQuestionInline(admin.TabularInline):
    model = ProductQuestion
    extra = 0
    readonly_fields = ('user', 'question', 'asked_at')
    fields = ('user', 'question', 'answer', 'asked_at', 'answered_at', 'is_public')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'farmer',
        'category',
        'price',
        'discount_price',
        'availability',
        'stock',
        'is_organic',
        'is_featured',
        'average_rating'
    )
    list_filter = (
        'category',
        'farmer',
        'availability',
        'is_organic',
        'is_featured',
        'created_at'
    )
    search_fields = ('name', 'description', 'farmer__farm_name')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ProductImageInline, ReviewInline, ProductQuestionInline]
    
    fieldsets = (
        ('Informacione Bazë', {
            'fields': (
                'name',
                'slug',
                'farmer',
                'category',
                'crop',
                'description'
            )
        }),
        ('Çmimi dhe Stoku', {
            'fields': (
                'price',
                'discount_price',
                'unit',
                'minimum_order',
                'stock',
                'availability'
            )
        }),
        ('Detaje Shtesë', {
            'fields': (
                'is_organic',
                'is_featured',
                'harvest_date',
                'expiry_date'
            )
        }),
        ('Informacione Sistemi', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def average_rating(self, obj):
        avg = obj.reviews.aggregate(Avg('rating'))['rating__avg']
        if avg:
            return f"{avg:.1f} / 5.0"
        return 'Pa vlerësime'
    average_rating.short_description = 'Vlerësimi mesatar'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'is_verified', 'created_at')
    list_filter = ('rating', 'is_verified', 'created_at')
    search_fields = ('product__name', 'user__username', 'comment')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(ProductQuestion)
class ProductQuestionAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'user',
        'short_question',
        'has_answer',
        'is_public',
        'asked_at'
    )
    list_filter = ('is_public', 'asked_at', 'answered_at')
    search_fields = ('product__name', 'user__username', 'question', 'answer')
    readonly_fields = ('asked_at',)
    
    def short_question(self, obj):
        return obj.question[:50] + '...' if len(obj.question) > 50 else obj.question
    short_question.short_description = 'Pyetja'
    
    def has_answer(self, obj):
        return bool(obj.answer)
    has_answer.boolean = True
    has_answer.short_description = 'Ka përgjigje'

    actions = ['make_public', 'make_private']

    def make_public(self, request, queryset):
        queryset.update(is_public=True)
    make_public.short_description = "Bëj publike pyetjet e zgjedhura"

    def make_private(self, request, queryset):
        queryset.update(is_public=False)
    make_private.short_description = "Bëj private pyetjet e zgjedhura"

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'show_image', 'is_primary', 'created_at')
    list_filter = ('is_primary', 'created_at')
    search_fields = ('product__name', 'alt_text')
    
    def show_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return '-'
    show_image.short_description = 'Imazhi'
