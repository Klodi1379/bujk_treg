from django.urls import path
from django.urls import path
from . import views
from django.conf.urls.i18n import i18n_patterns

app_name = 'logistics'

from . import views

app_name = 'logistics'

urlpatterns = [
    # Shipment URLs
    path('shipments/', views.ShipmentListView.as_view(), name='shipment_list'),
    path('shipments/create/', views.ShipmentCreateView.as_view(), name='shipment_create'),
    path('shipments/<int:pk>/', views.ShipmentDetailView.as_view(), name='shipment_detail'),
    path('shipments/<int:pk>/update/', views.ShipmentUpdateView.as_view(), name='shipment_update'),
    path('shipments/<int:pk>/delete/', views.ShipmentDeleteView.as_view(), name='shipment_delete'),
    path('shipments/<int:pk>/add-tracking/', views.add_tracking_event, name='add_tracking_event'),
    
    # Warehouse URLs
    path('warehouses/', views.WarehouseListView.as_view(), name='warehouse_list'),
    path('warehouses/create/', views.WarehouseCreateView.as_view(), name='warehouse_create'),
    path('warehouses/<int:pk>/', views.WarehouseDetailView.as_view(), name='warehouse_detail'),
    path('warehouses/<int:pk>/update/', views.WarehouseUpdateView.as_view(), name='warehouse_update'),
    path('warehouses/<int:pk>/delete/', views.WarehouseDeleteView.as_view(), name='warehouse_delete'),
    
    # Vehicle URLs
    path('vehicles/', views.VehicleListView.as_view(), name='vehicle_list'),
    path('vehicles/create/', views.VehicleCreateView.as_view(), name='vehicle_create'),
    path('vehicles/<int:pk>/', views.VehicleDetailView.as_view(), name='vehicle_detail'),
    path('vehicles/<int:pk>/update/', views.VehicleUpdateView.as_view(), name='vehicle_update'),
    path('vehicles/<int:pk>/delete/', views.VehicleDeleteView.as_view(), name='vehicle_delete'),
    
    # Transport Company URLs
    path('companies/', views.TransportCompanyListView.as_view(), name='transport_company_list'),
    path('companies/create/', views.TransportCompanyCreateView.as_view(), name='transport_company_create'),
    path('companies/<int:pk>/', views.TransportCompanyDetailView.as_view(), name='transport_company_detail'),
    path('companies/<int:pk>/update/', views.TransportCompanyUpdateView.as_view(), name='transport_company_update'),
    path('companies/<int:pk>/delete/', views.TransportCompanyDeleteView.as_view(), name='transport_company_delete'),

    # Driver URLs
    path('drivers/', views.DriverListView.as_view(), name='driver_list'),
    path('drivers/create/', views.DriverCreateView.as_view(), name='driver_create'),
    path('drivers/<int:pk>/', views.DriverDetailView.as_view(), name='driver_detail'),
    path('drivers/<int:pk>/update/', views.DriverUpdateView.as_view(), name='driver_update'),
    path('drivers/<int:pk>/delete/', views.DriverDeleteView.as_view(), name='driver_delete'),
    
    # Tracking URL
    path('track/', views.track_shipment, name='track_shipment'),
]
