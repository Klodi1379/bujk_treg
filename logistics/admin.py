from django.contrib import admin
from .models import (
    TransportCompany,
    Driver,
    Vehicle,
    Warehouse,
    Shipment,
    TrackingEvent
)

@admin.register(TransportCompany)
class TransportCompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'contact_email', 'contact_phone', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'contact_person', 'contact_email', 'registration_number', 'tax_number')
    ordering = ('name',)

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'license_number', 'license_expiry', 'is_available')
    list_filter = ('company', 'is_available', 'license_expiry')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'license_number')
    ordering = ('user__username',)
    raw_id_fields = ('user',)

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('plate_number', 'company', 'vehicle_type', 'model', 'capacity', 'availability')
    list_filter = ('company', 'vehicle_type', 'availability', 'year')
    search_fields = ('plate_number', 'model')
    ordering = ('plate_number',)

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'location', 'manager', 'capacity', 'current_utilization', 'is_active')
    list_filter = ('company', 'is_active', 'temperature_controlled', 'security_level')
    search_fields = ('name', 'location', 'manager')
    ordering = ('name',)

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ('capacity',)  # make capacity read-only
        return ()

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('tracking_number', 'company', 'status', 'priority', 'origin', 'destination', 'departure_date')
    list_filter = (
        'company',
        'status',
        'priority',
        'departure_date',
    )
    search_fields = ('tracking_number', 'origin', 'destination', 'sender_name', 'receiver_name')
    raw_id_fields = ('driver', 'vehicle', 'origin_warehouse', 'destination_warehouse')

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'tracking_number',
                'company',
                'status',
                'priority'
            )
        }),
        ('Route Information', {
            'fields': (
                ('origin', 'destination'),
                'current_location',
                ('origin_warehouse', 'destination_warehouse')
            )
        }),
        ('Schedule', {
            'fields': (
                'departure_date',
                'estimated_arrival',
                'actual_arrival'
            )
        }),
        ('Transport Details', {
            'fields': (
                'driver',
                'vehicle'
            )
        }),
        ('Package Information', {
            'fields': (
                ('weight', 'volume', 'package_count'),
                ('is_hazardous', 'requires_refrigeration'),
                'special_instructions'
            )
        }),
        ('Contact Information', {
            'fields': (
                ('sender_name', 'sender_phone'),
                ('receiver_name', 'receiver_phone')
            )
        }),
        ('Financial', {
            'fields': (
                'cost',
                'insurance_value'
            )
        })
    )

@admin.register(TrackingEvent)
class TrackingEventAdmin(admin.ModelAdmin):
    list_display = ('shipment', 'timestamp', 'location', 'status', 'recorded_by')
    list_filter = ('status', 'timestamp')
    search_fields = ('shipment__tracking_number', 'location', 'details')
    raw_id_fields = ('shipment', 'recorded_by')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)
