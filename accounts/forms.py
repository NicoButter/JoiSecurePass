from django import forms
from django.forms import inlineformset_factory

from .models import CustomUser, Address, Phone, NivelAcceso

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street_address', 'city', 'state', 'postal_code', 'country']

class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        fields = ['phone_number', 'phone_type']

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'dni', 'numero_legajo', 'nivel_acceso', 'profile_image']
        widgets = {
            'nivel_acceso': forms.Select(choices=[(nivel.id, nivel.nombre) for nivel in NivelAcceso.objects.all()]),
        }

AddressFormSet = inlineformset_factory(CustomUser, Address, form=AddressForm, extra=1, can_delete=True, max_num=5)
PhoneFormSet = inlineformset_factory(CustomUser, Phone, form=PhoneForm, extra=1, can_delete=True, max_num=5)