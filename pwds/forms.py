# pwds/forms.py
from django import forms
from .models import PWDProfile

class PWDProfileForm(forms.ModelForm):
    class Meta:
        model = PWDProfile
        fields = ['contact_number', 'disability_type', 'travel_needs']
