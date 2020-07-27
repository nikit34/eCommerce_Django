from django import forms
from django.utils.translation import gettext_lazy

from .models import MarketingPreference

class MarketingPreferenceForm(forms.ModelForm):
    subscribed = forms.BooleanField(label=gettext_lazy('Receive Marketing Email?'), required=False)
    class Meta:
        model = MarketingPreference
        fields = ['subscribed']
