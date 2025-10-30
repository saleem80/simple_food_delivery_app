from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'pickup_address', 'pickup_contact_name', 'pickup_contact_phone',
            'delivery_address', 'delivery_contact_name', 'delivery_contact_phone',
            'item_description', 'special_instructions', 'estimated_price'
        ]
        widgets = {
            'pickup_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter pickup address'
            }),
            'pickup_contact_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contact person name'
            }),
            'pickup_contact_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contact phone number'
            }),
            'delivery_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter delivery address'
            }),
            'delivery_contact_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contact person name'
            }),
            'delivery_contact_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contact phone number'
            }),
            'item_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe the items to be delivered'
            }),
            'special_instructions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Any special instructions (optional)'
            }),
            'estimated_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
        }