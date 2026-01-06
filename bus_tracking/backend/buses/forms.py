from django import forms
from .models import Bus, BusAssignment

class BusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = ['bus_number', 'license_plate', 'bus_type', 'capacity', 'model', 'year', 'is_active', 'current_route']
        widgets = {
            'bus_number': forms.TextInput(attrs={'class': 'form-control'}),
            'license_plate': forms.TextInput(attrs={'class': 'form-control'}),
            'bus_type': forms.Select(attrs={'class': 'form-select'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'current_route': forms.Select(attrs={'class': 'form-select'}),
        }


class BusAssignmentForm(forms.ModelForm):
    class Meta:
        model = BusAssignment
        fields = ['bus', 'driver', 'route']
        widgets = {
            'bus': forms.Select(attrs={'class': 'form-select'}),
            'driver': forms.Select(attrs={'class': 'form-select'}),
            'route': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from accounts.models import User
        self.fields['driver'].queryset = User.objects.filter(role='driver')
