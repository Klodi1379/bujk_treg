from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from .models import Order, CartItem, Transaction

class AddToCartForm(forms.ModelForm):
    """Forma për shtimin e produkteve në shportë"""
    class Meta:
        model = CartItem
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '0.1',
                    'step': '0.1'
                }
            )
        }

    def __init__(self, *args, product=None, **kwargs):
        super().__init__(*args, **kwargs)
        if product:
            self.fields['quantity'].validators.append(
                MinValueValidator(product.minimum_order)
            )
            self.fields['quantity'].widget.attrs.update({
                'min': product.minimum_order,
                'max': product.stock
            })

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if hasattr(self, 'product') and quantity > self.product.stock:
            raise forms.ValidationError(
                _('Sasia e kërkuar nuk është në dispozicion.')
            )
        return quantity

class UpdateCartItemForm(forms.ModelForm):
    """Forma për përditësimin e sasive në shportë"""
    class Meta:
        model = CartItem
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control'})
        }

class CheckoutForm(forms.ModelForm):
    """Forma për finalizimin e porosisë"""
    guest_name = forms.CharField(max_length=100, required=False, label=_('Emri'))
    guest_email = forms.EmailField(required=False, label=_('Email'))

    class Meta:
        model = Order
        fields = [
            'guest_name', # Guest user fields
            'guest_email',
            'shipping_address',
            'shipping_city',
            'shipping_phone',
            'payment_method',
            'notes'
        ]
        widgets = {
            'shipping_address': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': _('Shëno adresën e plotë të dorëzimit...')
                }
            ),
            'shipping_city': forms.TextInput(
                attrs={'placeholder': _('p.sh. Tiranë')}
            ),
            'shipping_phone': forms.TextInput(
                attrs={'placeholder': _('p.sh. +355 6X XXX XXXX')}
            ),
            'notes': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': _('Shënime shtesë për porosinë...')
                }
            )
        }

    def clean_shipping_phone(self):
        phone = self.cleaned_data['shipping_phone']
        # Pastro numrin e telefonit nga hapësirat dhe karakteret speciale
        phone = ''.join(filter(str.isdigit, phone))
        if not phone.startswith('355'):
            phone = '355' + phone
        return phone

class UpdateOrderStatusForm(forms.ModelForm):
    """Forma për përditësimin e statusit të porosisë"""
    class Meta:
        model = Order
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'})
        }

    def clean_status(self):
        new_status = self.cleaned_data['status']
        old_status = self.instance.status

        # Kontrollo nëse kalimi i statusit është i lejuar
        allowed_transitions = {
            'pending': ['confirmed', 'cancelled'],
            'confirmed': ['processing', 'cancelled'],
            'processing': ['shipping', 'cancelled'],
            'shipping': ['delivered', 'cancelled'],
            'delivered': [],  # Statusi final
            'cancelled': []   # Statusi final
        }

        if new_status not in allowed_transitions.get(old_status, []):
            raise forms.ValidationError(
                _('Ky ndryshim statusi nuk është i lejuar.')
            )

        return new_status

class PaymentForm(forms.ModelForm):
    """Forma për procesin e pagesës"""
    card_number = forms.CharField(
        label=_('Numri i kartës'),
        max_length=16,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'XXXX XXXX XXXX XXXX',
            'class': 'form-control'
        })
    )
    expiry_date = forms.CharField(
        label=_('Data e skadimit'),
        max_length=5,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'MM/YY',
            'class': 'form-control'
        })
    )
    cvv = forms.CharField(
        label=_('CVV'),
        max_length=4,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'XXX',
            'class': 'form-control'
        })
    )

    class Meta:
        model = Transaction
        fields = ['payment_method', 'notes']
        widgets = {
            'notes': forms.Textarea(
                attrs={
                    'rows': 2,
                    'placeholder': _('Shënime për pagesën...')
                }
            )
        }

    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get('payment_method')

        if payment_method == 'card':
            card_number = cleaned_data.get('card_number')
            expiry_date = cleaned_data.get('expiry_date')
            cvv = cleaned_data.get('cvv')

            if not all([card_number, expiry_date, cvv]):
                raise forms.ValidationError(
                    _('Të gjitha fushat e kartës janë të detyrueshme për pagesë me kartë.')
                )

            # Validimi i numrit të kartës
            if not card_number.isdigit() or len(card_number) not in [15, 16]:
                raise forms.ValidationError(
                    _('Numri i kartës është i pavlefshëm.')
                )

            # Validimi i datës së skadimit
            if '/' not in expiry_date:
                raise forms.ValidationError(
                    _('Formati i datës së skadimit duhet të jetë MM/YY.')
                )

            # Validimi i CVV
            if not cvv.isdigit() or len(cvv) not in [3, 4]:
                raise forms.ValidationError(
                    _('CVV është i pavlefshëm.')
                )

        return cleaned_data
