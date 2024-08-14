from django import forms
from .models import CustomUser, Address, Phone, NivelAcceso

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'dni', 'numero_legajo', 'nivel_acceso', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street_address', 'city', 'state', 'postal_code', 'country']

class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        fields = ['phone_number', 'phone_type']

class UserCreationForm(forms.ModelForm):
    address_set = forms.inlineformset_factory(CustomUser, Address, form=AddressForm, extra=1, can_delete=True)
    phone_set = forms.inlineformset_factory(CustomUser, Phone, form=PhoneForm, extra=1, can_delete=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'dni', 'numero_legajo', 'nivel_acceso', 'password']

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['address_set'].queryset = Address.objects.filter(user=self.instance)
            self.fields['phone_set'].queryset = Phone.objects.filter(user=self.instance)

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        if commit:
            user.save()
            addresses = self.cleaned_data.get('address_set')
            phones = self.cleaned_data.get('phone_set')
            for address in addresses:
                address.user = user
                address.save()
            for phone in phones:
                phone.user = user
                phone.save()
        return user
