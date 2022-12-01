# My Django Imports
from django import forms


# My App imports
from PAS_hallAllocation.models import (
    Venue,
)

from PAS_auth.models import(
    Programme,
)

class VenueForm(forms.ModelForm):
    venue_title = forms.CharField(help_text='Enter Venue Title',widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    prog_id = forms.ModelChoiceField(queryset=Programme.objects.all(), empty_label="(Select Programme Type)", required=True, help_text="Select Programme Type", widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))

    class Meta:
        model = Venue
        fields = ('venue_title', 'prog_id')

