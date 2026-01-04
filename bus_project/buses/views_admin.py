from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import BusRoute, Stopage, BusSchedule, UserProfile
from .forms import CreateUserForm


def staff_required(view_func):
    return user_passes_test(lambda u: u.is_staff)(view_func)


@login_required
@staff_required
def admin_dashboard(request):
    routes = BusRoute.objects.all().order_by("bus_number")
    return render(request, "buses/custom_admin/dashboard.html", {"routes": routes})


@login_required
@staff_required
def create_user(request):
    """Admin view to create new drivers and regular users"""
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            try:
                # Create the user
                user = User.objects.create_user(
                    username=form.cleaned_data["username"],
                    email=form.cleaned_data["email"],
                    password=form.cleaned_data["password"],
                    first_name=form.cleaned_data.get("first_name", ""),
                    last_name=form.cleaned_data.get("last_name", ""),
                )

                # Create the user profile with the selected role
                UserProfile.objects.create(user=user, role=form.cleaned_data["role"])

                role_display = (
                    "Driver" if form.cleaned_data["role"] == "DRIVER" else "User"
                )
                messages.success(
                    request,
                    f"User '{user.username}' created successfully as {role_display}. "
                    f"They can now login with their username and password.",
                )
                return redirect("buses:custom_admin_dashboard")
            except Exception as e:
                messages.error(request, f"Error creating user: {str(e)}")
    else:
        form = CreateUserForm()

    return render(request, "buses/custom_admin/create_user.html", {"form": form})
