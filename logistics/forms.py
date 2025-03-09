from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import (
    TransportCompany,
    Driver,
    Vehicle,
    Warehouse,
    Shipment,
    TrackingEvent
)

class DateInput(forms.DateInput):
    input_type = 'date'

class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

class TransportCompanyForm(forms.ModelForm):
    class Meta:
        model = TransportCompany
        fields = '__all__'
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = '__all__'
        widgets = {
            'license_expiry': DateInput(),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_license_expiry(self):
        expiry = self.cleaned_data.get('license_expiry')
        if expiry and expiry < timezone.now().date():
            raise ValidationError(_('License has expired'))
        return expiry

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'
        widgets = {
            'last_maintenance': DateInput(),
            'next_maintenance': DateInput(),
            'insurance_expiry': DateInput(),
            'availability': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        last_maintenance = cleaned_data.get('last_maintenance')
        next_maintenance = cleaned_data.get('next_maintenance')
        insurance_expiry = cleaned_data.get('insurance_expiry')

        if last_maintenance and next_maintenance and last_maintenance >= next_maintenance:
            raise ValidationError(_('Next maintenance date must be after last maintenance date'))

        if insurance_expiry and insurance_expiry < timezone.now().date():
            raise ValidationError(_('Insurance has expired'))

        return cleaned_data

class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = '__all__'
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'temperature_controlled': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        capacity = cleaned_data.get('capacity')
        current_utilization = cleaned_data.get('current_utilization')

        if capacity is not None and current_utilization is not None and current_utilization > capacity:
            raise ValidationError(_('Current utilization cannot exceed capacity'))

        return cleaned_data

class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = '__all__'
        widgets = {
            'departure_date': DateTimeInput(),
            'estimated_arrival': DateTimeInput(),
            'actual_arrival': DateTimeInput(),
            'special_instructions': forms.Textarea(attrs={'rows': 3}),
            'is_hazardous': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'requires_refrigeration': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show available drivers
        self.fields['driver'].queryset = Driver.objects.filter(is_available=True)
        # Only show available vehicles
        self.fields['vehicle'].queryset = Vehicle.objects.filter(availability=True)
        # Only show active warehouses
        warehouse_queryset = Warehouse.objects.filter(is_active=True)
        self.fields['origin_warehouse'].queryset = warehouse_queryset
        self.fields['destination_warehouse'].queryset = warehouse_queryset

    def clean(self):
        cleaned_data = super().clean()
        departure_date = cleaned_data.get('departure_date')
        estimated_arrival = cleaned_data.get('estimated_arrival')
        actual_arrival = cleaned_data.get('actual_arrival')
        requires_refrigeration = cleaned_data.get('requires_refrigeration')
        vehicle = cleaned_data.get('vehicle')
        volume = cleaned_data.get('volume')
        weight = cleaned_data.get('weight')

        if departure_date and estimated_arrival and departure_date >= estimated_arrival:
            raise ValidationError(_('Estimated arrival must be after departure date'))

        if actual_arrival and departure_date and actual_arrival <= departure_date:
            raise ValidationError(_('Actual arrival must be after departure date'))

        if requires_refrigeration and vehicle and vehicle.vehicle_type != 'refrigerated':
            raise ValidationError(_('Refrigerated shipments require a refrigerated vehicle'))

        if vehicle:
            if weight and weight > vehicle.capacity:
                raise ValidationError(_('Weight exceeds vehicle capacity'))

        # Check warehouse capacity
        origin_warehouse = cleaned_data.get('origin_warehouse')
        if origin_warehouse and volume:
            available_capacity = origin_warehouse.get_available_capacity()
            if volume > available_capacity:
                raise ValidationError(
                    _('Origin warehouse does not have enough capacity. Available: %(capacity)s m³'),
                    params={'capacity': available_capacity},
                )

        return cleaned_data

class TrackingEventForm(forms.ModelForm):
    class Meta:
        model = TrackingEvent
        fields = ['status', 'location', 'details']
        widgets = {
            'details': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        location = cleaned_data.get('location')

        if status and not location:
            raise ValidationError(_('Location is required when updating status'))

        return cleaned_data

class ShipmentSearchForm(forms.Form):
    FILTER_BY_CHOICES = [
        ('tracking_number', _('Tracking Number')),
        ('origin', _('Origin')),
        ('destination', _('Destination')),
        ('sender', _('Sender Name')),
        ('receiver', _('Receiver Name')),
    ]

    filter_by = forms.ChoiceField(
        choices=FILTER_BY_CHOICES,
        required=False,
        label=_('Filter By'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    search = forms.CharField(
        required=False,
        label=_('Search'),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter search term...')
        })
    )
    status = forms.ChoiceField(
        choices=[('', _('All Statuses'))] + list(Shipment.STATUS_CHOICES),
        required=False,
        label=_('Status'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    priority = forms.ChoiceField(
        choices=[('', _('All Priorities'))] + list(Shipment.PRIORITY_CHOICES),
        required=False,
        label=_('Priority'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    date_from = forms.DateField(
        required=False,
        label=_('From Date'),
        widget=DateInput(attrs={'class': 'form-control'})
    )
    date_to = forms.DateField(
        required=False,
        label=_('To Date'),
        widget=DateInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')

        if date_from and date_to and date_from > date_to:
            raise ValidationError(_('From date must be before to date'))

        return cleaned_data

class ShipmentTrackingForm(forms.Form):
    tracking_number = forms.CharField(
        max_length=50,
        label=_('Tracking Number'),
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': _('Enter tracking number'),
        })
    )
