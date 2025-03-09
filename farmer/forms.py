from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import (
    FarmerProfile,
    FarmLocation,
    Certification,
    FarmerCrop,
    ProductionLog
)

# 1. Forma për Regjistrimin e Përdoruesit
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True, max_length=30)
    last_name = forms.CharField(required=True, max_length=30)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('Ky email është përdorur tashmë.'))
        return email

# 2. Forma për Vendndodhjen e Fermës
class FarmLocationForm(forms.ModelForm):
    class Meta:
        model = FarmLocation
        fields = ['address', 'city', 'region', 'latitude', 'longitude']
        widgets = {
            'latitude': forms.NumberInput(attrs={'step': '0.000001'}),
            'longitude': forms.NumberInput(attrs={'step': '0.000001'})
        }

# 3. Forma për Profilin e Fermerit
class FarmerProfileForm(forms.ModelForm):
    class Meta:
        model = FarmerProfile
        exclude = ['user', 'is_verified', 'is_active', 'registration_date', 'last_modified']
        widgets = {
            'farm_description': forms.Textarea(attrs={'rows': 4}),
            'year_established': forms.NumberInput(attrs={'min': '1900', 'max': '2100'}),
            'total_land_area': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['farm_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control', 'placeholder': '+355XXXXXXXXX'})

# 4. Forma për Certifikatat
class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = ['name', 'issuing_organization', 'issue_date', 'expiry_date', 'document']
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'})
        }

    def clean(self):
        cleaned_data = super().clean()
        issue_date = cleaned_data.get('issue_date')
        expiry_date = cleaned_data.get('expiry_date')

        if issue_date and expiry_date and issue_date > expiry_date:
            raise forms.ValidationError(
                _('Data e skadimit duhet të jetë pas datës së lëshimit.')
            )
        return cleaned_data

# 5. Forma për Kulturat e Fermerit
class FarmerCropForm(forms.ModelForm):
    class Meta:
        model = FarmerCrop
        exclude = ['farmer']
        widgets = {
            'land_area': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'estimated_yield': forms.NumberInput(attrs={'step': '0.01', 'min': '0'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

# 6. Forma për Regjistrimin e Prodhimit
class ProductionLogForm(forms.ModelForm):
    class Meta:
        model = ProductionLog
        exclude = ['farmer', 'blockchain_hash', 'created_at', 'updated_at']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user and hasattr(user, 'farmer_profile'):
            # Filtro kulturat që i përkasin fermerit
            farmer_crops = FarmerCrop.objects.filter(farmer=user.farmer_profile)
            self.fields['crop'].queryset = farmer_crops.values_list('crop', flat=True)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

# 7. Forma për Përditësimin e Profilit të Fermerit
class FarmerProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = FarmerProfile
        fields = [
            'farm_name', 'farm_description', 'profile_image',
            'phone_number', 'website', 'total_land_area'
        ]
        widgets = {
            'farm_description': forms.Textarea(attrs={'rows': 4}),
            'total_land_area': forms.NumberInput(attrs={'step': '0.01', 'min': '0'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

# 8. Forma për Përditësimin e Vendndodhjes
class LocationUpdateForm(forms.ModelForm):
    class Meta:
        model = FarmLocation
        fields = ['address', 'city', 'region', 'latitude', 'longitude']
        widgets = {
            'latitude': forms.NumberInput(attrs={'step': '0.000001'}),
            'longitude': forms.NumberInput(attrs={'step': '0.000001'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})