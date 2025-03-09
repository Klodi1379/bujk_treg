from django.urls import path
from django.urls import path
from . import views
from django.conf.urls.i18n import i18n_patterns

app_name = 'farmer'

from . import views

app_name = 'farmer'

urlpatterns = [
    # Regjistrimi dhe profili
    path('login/', views.login_view, name='login'),
    path('register/', views.register_farmer, name='register'), # Ensure this points to register_farmer
    path('dashboard/', views.farmer_dashboard, name='dashboard'),
    path('profile/<int:pk>/', views.FarmerProfileDetailView.as_view(), name='profile_detail'),
    path('profile/<int:pk>/update/', views.FarmerProfileUpdateView.as_view(), name='profile_update'),
    path('location/update/', views.update_location, name='update_location'),
    
    # Certifikimet
    path('certification/add/', views.add_certification, name='add_certification'),
    
    # Kulturat
    path('crops/', views.manage_crops, name='manage_crops'),
    path('crop/<int:pk>/update/', views.FarmerCropUpdateView.as_view(), name='update_crop'),
    path('crop/<int:pk>/delete/', views.FarmerCropDeleteView.as_view(), name='delete_crop'),
    
    # Regjistrat e prodhimit
    path('logs/', views.ProductionLogListView.as_view(), name='production_logs'),
    path('logs/add/', views.add_production_log, name='add_production_log'),
    path('logs/<int:pk>/update/', views.ProductionLogUpdateView.as_view(), name='update_production_log'),
    path('logs/<int:pk>/delete/', views.ProductionLogDeleteView.as_view(), name='delete_crop'),
]
