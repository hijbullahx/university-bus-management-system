from django import forms
from django.contrib.auth.models import User
from .models import BusRoute, Stopage, UserProfile


class CreateUserForm(forms.Form):
    """Form to create new users (driver or regular user)"""

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "user@example.com"}
        ),
    )
    username = forms.CharField(
        max_length=150,
        label="Username",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter username"}
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter password"}
        ),
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm password"}
        ),
    )
    role = forms.ChoiceField(
        choices=[("USER", "Regular User"), ("DRIVER", "Driver")],
        label="User Role",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    first_name = forms.CharField(
        max_length=30,
        required=False,
        label="First Name",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "First name (optional)"}
        ),
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        label="Last Name",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Last name (optional)"}
        ),
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data


class StopageForm(forms.ModelForm):
    class Meta:
        model = Stopage
        fields = ["name", "pickup_time"]
        widgets = {
            "pickup_time": forms.TimeInput(attrs={"type": "time"}),
        }


StopageFormSet = forms.inlineformset_factory(
    BusRoute, Stopage, form=StopageForm, extra=1, can_delete=True
)


class BusRouteForm(forms.ModelForm):
    class Meta:
        model = BusRoute
        fields = ["bus_number", "route", "is_shuttle"]


class ShuttleRouteForm(forms.ModelForm):
    class Meta:
        model = BusRoute
        fields = ["bus_number", "route", "is_shuttle"]
        widgets = {
            "is_shuttle": forms.HiddenInput(),
        }
