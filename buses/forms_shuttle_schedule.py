from django import forms
from .models import BusRoute

class ShuttleScheduleForm(forms.Form):
    campus_departure = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label='Campus Departure')
    center_station_departure = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label='Route Departure')

ShuttleScheduleFormSet = forms.formset_factory(ShuttleScheduleForm, extra=0, can_delete=True)
