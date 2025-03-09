from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .models import Product, ProductImage, Review, ProductQuestion, Category

class ProductForm(forms.ModelForm):
    """Formë për krijimin dhe përditësimin e produkteve"""
    
    class Meta:
        model = Product
        fields = [
            'name', 'category', 'crop', 'description', 
            'price', 'discount_price', 'unit', 'minimum_order',
            'stock', 'availability', 'is_organic', 'harvest_date',
            'expiry_date'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'harvest_date': forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.farmer = kwargs.pop('farmer', None)
        super().__init__(*args, **kwargs)
        
        # Filtro kulturat në bazë të fermerit
        if self.farmer:
            self.fields['crop'].queryset = self.farmer.farmercrop_set.all()
        
        # Shto klasat për styling
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        discount_price = cleaned_data.get('discount_price')
        harvest_date = cleaned_data.get('harvest_date')
        expiry_date = cleaned_data.get('expiry_date')

        if discount_price and price and discount_price >= price:
            raise ValidationError(
                _('Çmimi me ulje duhet të jetë më i vogël se çmimi normal.')
            )

        if harvest_date and expiry_date and harvest_date > expiry_date:
            raise ValidationError(
                _('Data e skadencës duhet të jetë pas datës së vjeljes.')
            )

        return cleaned_data

    def save(self, commit=True):
        product = super().save(commit=False)
        if self.farmer:
            product.farmer = self.farmer
        if commit:
            product.save()
        return product

class ProductImageForm(forms.ModelForm):
    """Formë për ngarkimin e imazheve të produktit"""
    
    class Meta:
        model = ProductImage
        fields = ['image', 'is_primary', 'alt_text']
        widgets = {
            'alt_text': forms.TextInput(
                attrs={'placeholder': 'Përshkrim i shkurtër i imazhit'}
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        self.fields['alt_text'].widget.attrs.update({'class': 'form-control'})

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:  # 5MB limit
                raise ValidationError(
                    _('Madhësia maksimale e lejuar është 5MB.')
                )
        return image

class ReviewForm(forms.ModelForm):
    """Formë për vlerësimet e produkteve"""
    
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(
                attrs={
                    'min': '1',
                    'max': '5',
                    'class': 'form-control'
                }
            ),
            'comment': forms.Textarea(
                attrs={
                    'rows': 4,
                    'class': 'form-control',
                    'placeholder': 'Shkruani përshtypjet tuaja për produktin...'
                }
            )
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 5:
            raise ValidationError(
                _('Vlerësimi duhet të jetë nga 1 deri në 5.')
            )
        return rating

class ProductQuestionForm(forms.ModelForm):
    """Formë për pyetjet rreth produkteve"""
    
    class Meta:
        model = ProductQuestion
        fields = ['question']
        widgets = {
            'question': forms.Textarea(
                attrs={
                    'rows': 3,
                    'class': 'form-control',
                    'placeholder': 'Shkruani pyetjen tuaj rreth produktit...'
                }
            )
        }

class ProductAnswerForm(forms.ModelForm):
    """Formë për përgjigjet e pyetjeve"""
    
    class Meta:
        model = ProductQuestion
        fields = ['answer', 'is_public']
        widgets = {
            'answer': forms.Textarea(
                attrs={
                    'rows': 3,
                    'class': 'form-control',
                    'placeholder': 'Shkruani përgjigjen tuaj...'
                }
            )
        }

class ProductSearchForm(forms.Form):
    """Formë për kërkimin dhe filtrimin e produkteve"""
    
    q = forms.CharField(
        required=False,
        label=_('Kërko'),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Kërko produkte...'
            }
        )
    )
    category = forms.ModelChoiceField(
        required=False,
        queryset=Category.objects.all(),
        label=_('Kategoria'),
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )
    min_price = forms.DecimalField(
        required=False,
        label=_('Çmimi minimal'),
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nga'
            }
        )
    )
    max_price = forms.DecimalField(
        required=False,
        label=_('Çmimi maksimal'),
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Deri'
            }
        )
    )
    is_organic = forms.BooleanField(
        required=False,
        label=_('Vetëm produkte organike'),
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input'}
        )
    )
    in_stock = forms.BooleanField(
        required=False,
        label=_('Vetëm produkte në gjendje'),
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input'}
        )
    )
    sort = forms.ChoiceField(
        required=False,
        label=_('Rendit sipas'),
        choices=[
            ('', 'Zgjidhni...'),
            ('price_asc', 'Çmimi (i ulët në të lartë)'),
            ('price_desc', 'Çmimi (i lartë në të ulët)'),
            ('name', 'Emri (A-Z)'),
            ('name_desc', 'Emri (Z-A)'),
            ('rating', 'Vlerësimi'),
            ('date', 'Më të rejat'),
        ],
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        min_price = cleaned_data.get('min_price')
        max_price = cleaned_data.get('max_price')

        if min_price and max_price and min_price > max_price:
            raise ValidationError(
                _('Çmimi minimal nuk mund të jetë më i madh se çmimi maksimal.')
            )

        return cleaned_data
