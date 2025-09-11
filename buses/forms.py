from django import forms
from .models import BusRoute, Stopage

class StopageForm(forms.ModelForm):
    class Meta:
        model = Stopage
        fields = ['name', 'pickup_time', 'drop_time']
        widgets = {
            'pickup_time': forms.TimeInput(attrs={'type': 'time'}),
            'drop_time': forms.TimeInput(attrs={'type': 'time'}),
        }

StopageFormSet = forms.inlineformset_factory(
    BusRoute, Stopage, form=StopageForm, extra=1, can_delete=True
)

class BusRouteForm(forms.ModelForm):
    class Meta:
        model = BusRoute
        fields = ['bus_number', 'destination', 'description']
