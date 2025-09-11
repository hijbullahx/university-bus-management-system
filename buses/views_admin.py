from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from .models import BusRoute, Stopage, BusSchedule

def staff_required(view_func):
    return user_passes_test(lambda u: u.is_staff)(view_func)

@login_required
@staff_required
def admin_dashboard(request):
    routes = BusRoute.objects.all().order_by('bus_number')
    return render(request, 'buses/custom_admin/dashboard.html', {'routes': routes})
