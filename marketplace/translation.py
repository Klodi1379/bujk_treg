from modeltranslation.translator import register, TranslationOptions
from .models import Order, OrderItem, Transaction

@register(Order)
class OrderTranslationOptions(TranslationOptions):
    fields = ('shipping_address', 'shipping_city', 'notes',)

@register(OrderItem)
class OrderItemTranslationOptions(TranslationOptions):
    fields = ('product_name',)

@register(Transaction)
class TransactionTranslationOptions(TranslationOptions):
    fields = ('notes',)
