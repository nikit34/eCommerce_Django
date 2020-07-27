from django import forms
from django.utils.translation import gettext

from .models import Address
from .countries import countries_dict


class AddressForm(forms.ModelForm):
    def clean_country(self):
        country_code = self.cleaned_data.get('country')
        valid_code = False
        for country_union in countries_dict:
            if country_code == country_union['code']:
                valid_code = True
        if not valid_code:
            raise forms.ValidationError(gettext('Country code is not valid'))
        return country_code

    class Meta:
        model = Address
        fields = [
            'nickname',
            'name',
            # 'billing_profile',
            'address_type',
            'address_line_1',
            'address_line_2',
            'city',
            'country',
            'state',
            'postal_code'
        ]


class AddressCheckoutForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'nickname',
            'name',
            # 'billing_profile',
            # 'address_type',
            'address_line_1',
            'address_line_2',
            'city',
            'country',
            'state',
            'postal_code'
        ]
