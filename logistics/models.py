from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.conf import settings
from django.utils import timezone
from decimal import Decimal
import uuid

def default_estimated_arrival():
    return timezone.now() + timezone.timedelta(days=1)

class TransportCompany(models.Model):
    company_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    name_en = models.CharField(max_length=100, verbose_name=_('Name'), null=True, blank=True)
    name_sq = models.CharField(max_length=100, verbose_name=_('Name'), null=True, blank=True)
    contact_person = models.CharField(max_length=100, verbose_name=_('Contact Person'))
    contact_person_en = models.CharField(max_length=100, verbose_name=_('Contact Person'), null=True, blank=True)
    contact_person_sq = models.CharField(max_length=100, verbose_name=_('Contact Person'), null=True, blank=True)
    contact_email = models.EmailField(verbose_name=_('Contact Email'))
    contact_phone = models.CharField(max_length=20, verbose_name=_('Contact Phone'))
    address = models.TextField(verbose_name=_('Address'))
    address_en = models.TextField(verbose_name=_('Address'), null=True, blank=True)
    address_sq = models.TextField(verbose_name=_('Address'), null=True, blank=True)
    registration_number = models.CharField(max_length=50, verbose_name=_('Registration Number'))
    tax_number = models.CharField(max_length=50, verbose_name=_('Tax Number'))
    website = models.URLField(blank=True, null=True, verbose_name=_('Website'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))

    class Meta:
        verbose_name = _('Transport Company')
        verbose_name_plural = _('Transport Companies')

    def __str__(self):
        return self.name

class Driver(models.Model):
    driver_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='driver_profile')
    company = models.ForeignKey(TransportCompany, on_delete=models.CASCADE, related_name='drivers')
    license_number = models.CharField(max_length=50, verbose_name=_('License Number'))
    license_expiry = models.DateField(verbose_name=_('License Expiry Date'))
    phone = models.CharField(max_length=20, verbose_name=_('Phone Number'))
    emergency_contact = models.CharField(max_length=100, verbose_name=_('Emergency Contact'))
    emergency_contact_en = models.CharField(max_length=100, verbose_name=_('Emergency Contact'), null=True, blank=True)
    emergency_contact_sq = models.CharField(max_length=100, verbose_name=_('Emergency Contact'), null=True, blank=True)
    emergency_phone = models.CharField(max_length=20, verbose_name=_('Emergency Phone'))
    is_available = models.BooleanField(default=True, verbose_name=_('Is Available'))

    class Meta:
        verbose_name = _('Driver')
        verbose_name_plural = _('Drivers')

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.license_number}"

class Vehicle(models.Model):
    VEHICLE_TYPES = [
        ('truck', _('Truck')),
        ('van', _('Van')),
        ('refrigerated', _('Refrigerated Truck')),
        ('pickup', _('Pickup Truck')),
    ]

    vehicle_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(TransportCompany, on_delete=models.CASCADE, related_name='vehicles')
    vehicle_type = models.CharField(max_length=50, choices=VEHICLE_TYPES, verbose_name=_('Vehicle Type'))
    plate_number = models.CharField(max_length=20, unique=True, verbose_name=_('Plate Number'))
    model = models.CharField(max_length=100, verbose_name=_('Model'))
    model_en = models.CharField(max_length=100, verbose_name=_('Model'), null=True, blank=True)
    model_sq = models.CharField(max_length=100, verbose_name=_('Model'), null=True, blank=True)
    year = models.IntegerField(verbose_name=_('Year'))
    capacity = models.FloatField(validators=[MinValueValidator(0)], verbose_name=_('Capacity (kg)'))
    availability = models.BooleanField(default=True, verbose_name=_('Is Available'))
    last_maintenance = models.DateField(verbose_name=_('Last Maintenance Date'))
    next_maintenance = models.DateField(verbose_name=_('Next Maintenance Date'))
    insurance_expiry = models.DateField(verbose_name=_('Insurance Expiry Date'))
    current_location = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Current Location'))
    current_location_en = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Current Location'))
    current_location_sq = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Current Location'))

    class Meta:
        verbose_name = _('Vehicle')
        verbose_name_plural = _('Vehicles')

    def __str__(self):
        return f"{self.get_vehicle_type_display()} - {self.plate_number}"

class Warehouse(models.Model):
    SECURITY_LEVELS = [
        ('low', _('Low')),
        ('medium', _('Medium')),
        ('high', _('High')),
        ('maximum', _('Maximum')),
    ]

    warehouse_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(TransportCompany, on_delete=models.CASCADE, related_name='warehouses')
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    name_en = models.CharField(max_length=100, verbose_name=_('Name'), null=True, blank=True)
    name_sq = models.CharField(max_length=100, verbose_name=_('Name'), null=True, blank=True)
    location = models.CharField(max_length=100, verbose_name=_('Location'))
    location_en = models.CharField(max_length=100, verbose_name=_('Location'), null=True, blank=True)
    location_sq = models.CharField(max_length=100, verbose_name=_('Location'), null=True, blank=True)
    address = models.TextField(verbose_name=_('Address'))
    address_en = models.TextField(verbose_name=_('Address'), null=True, blank=True)
    address_sq = models.TextField(verbose_name=_('Address'), null=True, blank=True)
    capacity = models.FloatField(validators=[MinValueValidator(0)], verbose_name=_('Capacity (m³)'))
    current_utilization = models.FloatField(default=0, validators=[MinValueValidator(0)], verbose_name=_('Current Utilization (m³)'))
    manager = models.CharField(max_length=100, verbose_name=_('Manager'))
    manager_en = models.CharField(max_length=100, verbose_name=_('Manager'), null=True, blank=True)
    manager_sq = models.CharField(max_length=100, verbose_name=_('Manager'), null=True, blank=True)
    contact_phone = models.CharField(max_length=20, verbose_name=_('Contact Phone'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))
    temperature_controlled = models.BooleanField(default=False, verbose_name=_('Temperature Controlled'))
    security_level = models.CharField(max_length=50, choices=SECURITY_LEVELS, default='medium', verbose_name=_('Security Level'))

    class Meta:
        verbose_name = _('Warehouse')
        verbose_name_plural = _('Warehouses')

    def __str__(self):
        return f"{self.name} - {self.location}"

    def get_available_capacity(self):
        return self.capacity - self.current_utilization

    def get_utilization_percentage(self):
        if self.capacity > 0:
            return round((self.current_utilization / self.capacity) * 100, 1)
        return 0

def generate_tracking_number():
    return str(uuid.uuid4().hex[:10].upper())

class Shipment(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('picking_up', _('Picking Up')),
        ('picked_up', _('Picked Up')),
        ('in_transit', _('In Transit')),
        ('at_warehouse', _('At Warehouse')),
        ('out_for_delivery', _('Out for Delivery')),
        ('delivered', _('Delivered')),
        ('delayed', _('Delayed')),
        ('cancelled', _('Cancelled')),
    ]

    PRIORITY_CHOICES = [
        ('low', _('Low')),
        ('medium', _('Medium')),
        ('high', _('High')),
        ('urgent', _('Urgent')),
    ]

    shipment_id = models.AutoField(primary_key=True)
    tracking_number = models.CharField(max_length=50, unique=True, default=generate_tracking_number, verbose_name=_('Tracking Number'))
    company = models.ForeignKey(TransportCompany, on_delete=models.PROTECT, related_name='shipments', verbose_name=_('Transport Company'))
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name='shipments')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True, related_name='shipments')
    origin_warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, blank=True, related_name='outbound_shipments')
    destination_warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, blank=True, related_name='inbound_shipments')
    
    origin = models.CharField(max_length=100, verbose_name=_('Origin'))
    origin_en = models.CharField(max_length=100, verbose_name=_('Origin'), null=True, blank=True)
    origin_sq = models.CharField(max_length=100, verbose_name=_('Origin'), null=True, blank=True)
    destination = models.CharField(max_length=100, verbose_name=_('Destination'))
    destination_en = models.CharField(max_length=100, verbose_name=_('Destination'), null=True, blank=True)
    destination_sq = models.CharField(max_length=100, verbose_name=_('Destination'), null=True, blank=True)
    sender_name = models.CharField(max_length=100, verbose_name=_('Sender Name'))
    sender_name_en = models.CharField(max_length=100, verbose_name=_('Sender Name'), null=True, blank=True)
    sender_name_sq = models.CharField(max_length=100, verbose_name=_('Sender Name'), null=True, blank=True)
    sender_phone = models.CharField(max_length=20, verbose_name=_('Sender Phone'))
    receiver_name = models.CharField(max_length=100, verbose_name=_('Receiver Name'))
    receiver_name_en = models.CharField(max_length=100, verbose_name=_('Receiver Name'), null=True, blank=True)
    receiver_name_sq = models.CharField(max_length=100, verbose_name=_('Receiver Name'), null=True, blank=True)
    receiver_phone = models.CharField(max_length=20, verbose_name=_('Receiver Phone'))
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name=_('Status'))
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium', verbose_name=_('Priority'))
    
    departure_date = models.DateTimeField(default=timezone.now, verbose_name=_('Departure Date'))
    estimated_arrival = models.DateTimeField(default=default_estimated_arrival, verbose_name=_('Estimated Arrival'))
    actual_arrival = models.DateTimeField(null=True, blank=True, verbose_name=_('Actual Arrival'))
    
    weight = models.FloatField(default=0, validators=[MinValueValidator(0)], verbose_name=_('Weight (kg)'))
    volume = models.FloatField(default=0, validators=[MinValueValidator(0)], verbose_name=_('Volume (m³)'))
    package_count = models.IntegerField(default=1, validators=[MinValueValidator(1)], verbose_name=_('Package Count'))
    
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name=_('Cost'))
    insurance_value = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name=_('Insurance Value'))
    
    special_instructions = models.TextField(blank=True, null=True, verbose_name=_('Special Instructions'))
    special_instructions_en = models.TextField(blank=True, null=True, verbose_name=_('Special Instructions'))
    special_instructions_sq = models.TextField(blank=True, null=True, verbose_name=_('Special Instructions'))
    current_location = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Current Location'))

    class Meta:
        verbose_name = _('Shipment')
        verbose_name_plural = _('Shipments')

    def __str__(self):
        return f"Shipment {self.tracking_number} - {self.origin} to {self.destination}"

    def update_status(self, new_status, location=None, details=None):
        self.status = new_status
        if location:
            self.current_location = location
        self.save()
        
        # Create tracking event
        TrackingEvent.objects.create(
            shipment=self,
            status=new_status,
            location=location or self.current_location,
            details=details
        )

class TrackingEvent(models.Model):
    event_id = models.AutoField(primary_key=True)
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='tracking_events')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_('Timestamp'))
    location = models.CharField(max_length=100, verbose_name=_('Location'))
    location_en = models.CharField(max_length=100, verbose_name=_('Location'), null=True, blank=True)
    location_sq = models.CharField(max_length=100, verbose_name=_('Location'), null=True, blank=True)
    status = models.CharField(max_length=20, choices=Shipment.STATUS_CHOICES, verbose_name=_('Status'))
    details = models.TextField(blank=True, null=True, verbose_name=_('Details'))
    details_en = models.TextField(blank=True, null=True, verbose_name=_('Details'))
    details_sq = models.TextField(blank=True, null=True, verbose_name=_('Details'))
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name=_('Recorded By'))

    class Meta:
        ordering = ['-timestamp']
        verbose_name = _('Tracking Event')
        verbose_name_plural = _('Tracking Events')

    def __str__(self):
        return f"{self.shipment.tracking_number} - {self.timestamp} - {self.status}"
