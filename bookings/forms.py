from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['driver', 'destination', 'pickup_location', 'travel_date', 'travel_time']
