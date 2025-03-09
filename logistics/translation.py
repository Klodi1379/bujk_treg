from modeltranslation.translator import register, TranslationOptions
from .models import TransportCompany, Driver, Vehicle, Warehouse, Shipment, TrackingEvent

@register(TransportCompany)
class TransportCompanyTranslationOptions(TranslationOptions):
    fields = ('name', 'contact_person', 'address',)

@register(Driver)
class DriverTranslationOptions(TranslationOptions):
    fields = ('emergency_contact',)

@register(Vehicle)
class VehicleTranslationOptions(TranslationOptions):
    fields = ('model', 'current_location',)

@register(Warehouse)
class WarehouseTranslationOptions(TranslationOptions):
    fields = ('name', 'location', 'address', 'manager',)

@register(Shipment)
class ShipmentTranslationOptions(TranslationOptions):
    fields = ('origin', 'destination', 'sender_name', 'receiver_name', 'special_instructions', 'current_location',)

@register(TrackingEvent)
class TrackingEventTranslationOptions(TranslationOptions):
    fields = ('location', 'details',)
