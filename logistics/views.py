from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages
from .models import (
    Shipment,
    TrackingEvent,
    Warehouse,
    Vehicle,
    TransportCompany,
    Driver
)
from .forms import (
    ShipmentForm,
    WarehouseForm,
    VehicleForm,
    TransportCompanyForm,
    DriverForm,
    TrackingEventForm,
    ShipmentSearchForm,
    ShipmentTrackingForm
)

class LogisticsStaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or hasattr(self.request.user, 'driver_profile')

class ShipmentListView(LoginRequiredMixin, ListView):
    model = Shipment
    template_name = 'logistics/shipment_list.html'
    context_object_name = 'shipments'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        form = ShipmentSearchForm(self.request.GET)

        if form.is_valid():
            status = form.cleaned_data.get('status')
            priority = form.cleaned_data.get('priority')
            date_from = form.cleaned_data.get('date_from')
            date_to = form.cleaned_data.get('date_to')
            search = form.cleaned_data.get('search')

            if status:
                queryset = queryset.filter(status=status)
            if priority:
                queryset = queryset.filter(priority=priority)
            if date_from:
                queryset = queryset.filter(departure_date__gte=date_from)
            if date_to:
                queryset = queryset.filter(departure_date__lte=date_to)
            if search:
                queryset = queryset.filter(
                    Q(tracking_number__icontains=search) |
                    Q(origin__icontains=search) |
                    Q(destination__icontains=search)
                )

        # If user is a driver, only show their shipments
        if hasattr(self.request.user, 'driver_profile'):
            queryset = queryset.filter(driver=self.request.user.driver_profile)

        return queryset.select_related('company', 'driver', 'vehicle')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = ShipmentSearchForm(self.request.GET)
        return context

class ShipmentDetailView(LoginRequiredMixin, DetailView):
    model = Shipment
    template_name = 'logistics/shipment_detail.html'
    context_object_name = 'shipment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tracking_events'] = self.object.tracking_events.all().select_related('recorded_by')
        if self.request.user.is_staff or hasattr(self.request.user, 'driver_profile'):
            context['tracking_form'] = TrackingEventForm()
        return context

class ShipmentCreateView(LogisticsStaffRequiredMixin, SuccessMessageMixin, CreateView):
    model = Shipment
    form_class = ShipmentForm
    template_name = 'logistics/shipment_form.html'
    success_url = reverse_lazy('logistics:shipment_list')
    success_message = _("Shipment was created successfully")

class ShipmentUpdateView(LogisticsStaffRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Shipment
    form_class = ShipmentForm
    template_name = 'logistics/shipment_form.html'
    success_url = reverse_lazy('logistics:shipment_list')
    success_message = _("Shipment was updated successfully")

class ShipmentDeleteView(LogisticsStaffRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Shipment
    template_name = 'logistics/shipment_confirm_delete.html'
    success_url = reverse_lazy('logistics:shipment_list')
    success_message = _("Shipment was deleted successfully")

def track_shipment(request):
    form = ShipmentTrackingForm(request.GET or None)
    shipment = None
    tracking_events = None

    if form.is_valid():
        tracking_number = form.cleaned_data['tracking_number']
        try:
            shipment = Shipment.objects.get(tracking_number=tracking_number)
            tracking_events = shipment.tracking_events.all()
        except Shipment.DoesNotExist:
            messages.error(request, _("No shipment found with this tracking number"))

    return render(request, 'logistics/tracking.html', {
        'form': form,
        'shipment': shipment,
        'tracking_events': tracking_events
    })

class WarehouseListView(LoginRequiredMixin, ListView):
    model = Warehouse
    template_name = 'logistics/warehouse_list.html'
    context_object_name = 'warehouses'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(location__icontains=search)
            )
        return queryset.select_related('company')

class WarehouseDetailView(LoginRequiredMixin, DetailView):
    model = Warehouse
    template_name = 'logistics/warehouse_detail.html'
    context_object_name = 'warehouse'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inbound_shipments'] = self.object.inbound_shipments.all()
        context['outbound_shipments'] = self.object.outbound_shipments.all()
        return context

class WarehouseCreateView(LogisticsStaffRequiredMixin, SuccessMessageMixin, CreateView):
    model = Warehouse
    form_class = WarehouseForm
    template_name = 'logistics/warehouse_form.html'
    success_url = reverse_lazy('logistics:warehouse_list')
    success_message = _("Warehouse was created successfully")

class WarehouseUpdateView(LogisticsStaffRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Warehouse
    form_class = WarehouseForm
    template_name = 'logistics/warehouse_form.html'
    success_url = reverse_lazy('logistics:warehouse_list')
    success_message = _("Warehouse was updated successfully")

class WarehouseDeleteView(LogisticsStaffRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Warehouse
    template_name = 'logistics/warehouse_confirm_delete.html'
    success_url = reverse_lazy('logistics:warehouse_list')
    success_message = _("Warehouse was deleted successfully")

class VehicleListView(LoginRequiredMixin, ListView):
    model = Vehicle
    template_name = 'logistics/vehicle_list.html'
    context_object_name = 'vehicles'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by search term
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(plate_number__icontains=search) |
                Q(model__icontains=search)
            )

        # Filter by vehicle type
        vehicle_type = self.request.GET.get('type')
        if vehicle_type:
            queryset = queryset.filter(vehicle_type=vehicle_type)

        # Filter by availability
        availability = self.request.GET.get('availability')
        if availability == 'true':
            queryset = queryset.filter(availability=True)
        elif availability == 'false':
            queryset = queryset.filter(availability=False)

        return queryset.select_related('company')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehicle_types'] = Vehicle.VEHICLE_TYPES
        context['now'] = timezone.now()
        return context

class VehicleDetailView(LoginRequiredMixin, DetailView):
    model = Vehicle
    template_name = 'logistics/vehicle_detail.html'
    context_object_name = 'vehicle'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_shipment'] = self.object.shipments.filter(
            status__in=['picking_up', 'picked_up', 'in_transit', 'out_for_delivery']
        ).first()
        context['now'] = timezone.now()
        return context

class VehicleCreateView(LogisticsStaffRequiredMixin, SuccessMessageMixin, CreateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'logistics/vehicle_form.html'
    success_url = reverse_lazy('logistics:vehicle_list')
    success_message = _("Vehicle was created successfully")

class VehicleUpdateView(LogisticsStaffRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'logistics/vehicle_form.html'
    success_url = reverse_lazy('logistics:vehicle_list')
    success_message = _("Vehicle was updated successfully")

class VehicleDeleteView(LogisticsStaffRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Vehicle
    template_name = 'logistics/vehicle_confirm_delete.html'
    success_url = reverse_lazy('logistics:vehicle_list')
    success_message = _("Vehicle was deleted successfully")

class TransportCompanyListView(LoginRequiredMixin, ListView):
    model = TransportCompany
    template_name = 'logistics/transportcompany_list.html'
    context_object_name = 'transport_companies'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(contact_person__icontains=search)
            )
        return queryset

class TransportCompanyDetailView(LoginRequiredMixin, DetailView):
    model = TransportCompany
    template_name = 'logistics/transportcompany_detail.html'
    context_object_name = 'transport_company'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehicles'] = self.object.vehicles.all()
        context['warehouses'] = self.object.warehouses.all()
        context['drivers'] = self.object.drivers.all()
        return context

class TransportCompanyCreateView(LogisticsStaffRequiredMixin, SuccessMessageMixin, CreateView):
    model = TransportCompany
    form_class = TransportCompanyForm
    template_name = 'logistics/transportcompany_form.html'
    success_url = reverse_lazy('logistics:transport_company_list')
    success_message = _("Transport company was created successfully")

class TransportCompanyUpdateView(LogisticsStaffRequiredMixin, SuccessMessageMixin, UpdateView):
    model = TransportCompany
    form_class = TransportCompanyForm
    template_name = 'logistics/transportcompany_form.html'
    success_url = reverse_lazy('logistics:transport_company_list')
    success_message = _("Transport company was updated successfully")

class TransportCompanyDeleteView(LogisticsStaffRequiredMixin, SuccessMessageMixin, DeleteView):
    model = TransportCompany
    template_name = 'logistics/transportcompany_confirm_delete.html'
    success_url = reverse_lazy('logistics:transport_company_list')
    success_message = _("Transport company was deleted successfully")

class DriverListView(LoginRequiredMixin, ListView):
    model = Driver
    template_name = 'logistics/driver_list.html'
    context_object_name = 'drivers'

class DriverDetailView(LoginRequiredMixin, DetailView):
    model = Driver
    template_name = 'logistics/driver_detail.html'
    context_object_name = 'driver'

class DriverCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Driver
    form_class = DriverForm
    template_name = 'logistics/driver_form.html'
    success_url = reverse_lazy('logistics:driver_list')
    success_message = _("Driver was created successfully")

class DriverUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Driver
    form_class = DriverForm
    template_name = 'logistics/driver_form.html'
    success_url = reverse_lazy('logistics:driver_list')
    success_message = _("Driver was updated successfully")

class DriverDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Driver
    template_name = 'logistics/driver_confirm_delete.html'
    success_url = reverse_lazy('logistics:driver_list')
    success_message = _("Driver was deleted successfully")

def add_tracking_event(request, pk):
    if not (request.user.is_staff or hasattr(request.user, 'driver_profile')):
        messages.error(request, _("You don't have permission to add tracking events"))
        return redirect('logistics:shipment_detail', pk=pk)

    shipment = get_object_or_404(Shipment, pk=pk)
    
    if request.method == 'POST':
        form = TrackingEventForm(request.POST)
        if form.is_valid():
            tracking_event = form.save(commit=False)
            tracking_event.shipment = shipment
            tracking_event.recorded_by = request.user
            tracking_event.save()
            
            # Update shipment status
            shipment.update_status(
                tracking_event.status,
                tracking_event.location,
                tracking_event.details
            )
            
            messages.success(request, _("Tracking event was added successfully"))
            return redirect('logistics:shipment_detail', pk=pk)
    else:
        form = TrackingEventForm()

    return render(request, 'logistics/tracking_event_form.html', {
        'form': form,
        'shipment': shipment
    })
