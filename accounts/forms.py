from django import forms
from .models import User


class LoginForm(forms.Form):
    mobile_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter mobile number',
            'required': True
        })
    )
    user_type = forms.ChoiceField(
        choices=User.USER_TYPE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': True
        })
    )


class OTPForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        min_length=4,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter OTP',
            'required': True,
            'pattern': '[0-9]{4,6}'
        })
    )


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['mobile_number', 'first_name', 'last_name', 'user_type']
        widgets = {
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'user_type': forms.Select(attrs={'class': 'form-control'}),
        }