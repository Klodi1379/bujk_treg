from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, _('Mirë se erdhët!'))
            return redirect('farmer:dashboard')
        else:
            messages.error(request, _('Emri i përdoruesit ose fjalëkalimi është i pasaktë.'))
    
    return render(request, 'farmer/login.html')

from .models import (
    FarmerProfile,
    FarmLocation,
    Certification,
    Crop,
    FarmerCrop,
    ProductionLog
)
from .forms import (
    UserRegistrationForm,
    FarmerProfileForm,
    FarmLocationForm,
    CertificationForm,
    FarmerCropForm,
    ProductionLogForm,
    FarmerProfileUpdateForm,
    LocationUpdateForm
)

def register_farmer(request): # Changed to function-based view
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = FarmerProfileForm(request.POST, request.FILES)
        location_form = FarmLocationForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid() and location_form.is_valid():
            # Krijo përdoruesin
            user = user_form.save()

            # Krijo vendndodhjen
            location = location_form.save()

            # Krijo profilin e fermerit
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.location = location
            profile.save()

            # Ruaj metodat e kultivimit dhe certifikimet
            profile_form.save_m2m()

            messages.success(request, _('Regjistrimi u krye me sukses! Tani mund të identifikoheni.'))
            return redirect('farmer:login')
    else:
        user_form = UserRegistrationForm()
        profile_form = FarmerProfileForm()
        location_form = FarmLocationForm()

    context = { # Pass forms in context
        'user_form': user_form,
        'profile_form': profile_form,
        'location_form': location_form
    }
    return render(request, 'farmer/register.html', context) # Render template with context

@login_required
def farmer_dashboard(request):
    try:
        farmer = request.user.farmer_profile
    except FarmerProfile.DoesNotExist:
        return redirect('farmer:register')
    
    # Merr statistikat
    total_crops = FarmerCrop.objects.filter(farmer=farmer).count()
    total_area = FarmerCrop.objects.filter(farmer=farmer).aggregate(
        total=Sum('land_area')
    )['total'] or 0
    recent_logs = ProductionLog.objects.filter(
        farmer=farmer
    ).select_related('crop').order_by('-date')[:5]
    
    context = {
        'farmer': farmer,
        'total_crops': total_crops,
        'total_area': total_area,
        'recent_logs': recent_logs,
    }
    
    return render(request, 'farmer/dashboard.html', context)

class FarmerProfileDetailView(DetailView):
    model = FarmerProfile
    template_name = 'farmer/profile_detail.html'
    context_object_name = 'farmer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        farmer = self.object
        context['crops'] = FarmerCrop.objects.filter(farmer=farmer).select_related('crop')
        context['certifications'] = farmer.certifications.all()
        return context

class FarmerProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = FarmerProfile
    form_class = FarmerProfileUpdateForm
    template_name = 'farmer/profile_update.html'
    success_url = reverse_lazy('farmer:dashboard')

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user

    def form_valid(self, form):
        messages.success(self.request, _('Profili u përditësua me sukses!'))
        return super().form_valid(form)

@login_required
def update_location(request):
    try:
        farmer = request.user.farmer_profile
        location = farmer.location
    except FarmerProfile.DoesNotExist:
        return redirect('farmer:register')
    
    if request.method == 'POST':
        form = LocationUpdateForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            messages.success(request, _('Vendndodhja u përditësua me sukses!'))
            return redirect('farmer:dashboard')
    else:
        form = LocationUpdateForm(instance=location)
    
    return render(request, 'farmer/location_update.html', {'form': form})

@login_required
def add_certification(request):
    if request.method == 'POST':
        form = CertificationForm(request.POST, request.FILES)
        if form.is_valid():
            certification = form.save()
            request.user.farmer_profile.certifications.add(certification)
            messages.success(request, _('Certifikimi u shtua me sukses!'))
            return redirect('farmer:dashboard')
    else:
        form = CertificationForm()
    
    return render(request, 'farmer/certification_form.html', {'form': form})

@login_required
def manage_crops(request):
    farmer = request.user.farmer_profile
    if request.method == 'POST':
        form = FarmerCropForm(request.POST)
        if form.is_valid():
            farmer_crop = form.save(commit=False)
            farmer_crop.farmer = farmer
            farmer_crop.save()
            messages.success(request, _('Kultura u shtua me sukses!'))
            return redirect('farmer:manage_crops')
    else:
        form = FarmerCropForm()
    
    farmer_crops = FarmerCrop.objects.filter(farmer=farmer).select_related('crop', 'cultivation_method')
    
    return render(request, 'farmer/manage_crops.html', {
        'form': form,
        'farmer_crops': farmer_crops
    })

class FarmerCropUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = FarmerCrop
    form_class = FarmerCropForm
    template_name = 'farmer/crop_update.html'
    success_url = reverse_lazy('farmer:manage_crops')

    def test_func(self):
        crop = self.get_object()
        return self.request.user == crop.farmer.user

    def form_valid(self, form):
        messages.success(self.request, _('Kultura u përditësua me sukses!'))
        return super().form_valid(form)

class FarmerCropDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = FarmerCrop
    template_name = 'farmer/crop_confirm_delete.html'
    success_url = reverse_lazy('farmer:manage_crops')

    def test_func(self):
        crop = self.get_object()
        return self.request.user == crop.farmer.user

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, _('Kultura u fshi me sukses!'))
        return super().delete(request, *args, **kwargs)

@login_required
def add_production_log(request):
    if request.method == 'POST':
        form = ProductionLogForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            log = form.save(commit=False)
            log.farmer = request.user.farmer_profile
            log.save()
            messages.success(request, _('Regjistri i prodhimit u shtua me sukses!'))
            return redirect('farmer:production_logs')
    else:
        form = ProductionLogForm(request.user)
    
    return render(request, 'farmer/production_log_form.html', {'form': form})

class ProductionLogListView(LoginRequiredMixin, ListView):
    model = ProductionLog
    template_name = 'farmer/production_logs.html'
    context_object_name = 'logs'
    paginate_by = 10

    def get_queryset(self):
        return ProductionLog.objects.filter(
            farmer=self.request.user.farmer_profile
        ).select_related('crop').order_by('-date')

class ProductionLogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ProductionLog
    form_class = ProductionLogForm
    template_name = 'farmer/production_log_form.html'
    success_url = reverse_lazy('farmer:production_logs')

    def test_func(self):
        log = self.get_object()
        return self.request.user == log.farmer.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, _('Regjistri u përditësua me sukses!'))
        return super().form_valid(form)

class ProductionLogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ProductionLog
    template_name = 'farmer/production_log_confirm_delete.html'
    success_url = reverse_lazy('farmer:production_logs')

    def test_func(self):
        log = self.get_object()
        return self.request.user == log.farmer.user

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, _('Regjistri u fshi me sukses!'))
        return super().delete(request, *args, **kwargs)
