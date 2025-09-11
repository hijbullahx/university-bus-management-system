from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import BusRoute, Stopage
from .forms import BusRouteForm, StopageFormSet
from .views_admin import staff_required

@login_required
@staff_required
def create_route(request):
    if request.method == 'POST':
        form = BusRouteForm(request.POST)
        formset = StopageFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            route = form.save()
            formset.instance = route
            formset.save()
            return redirect('buses:custom_admin_dashboard')
    else:
        form = BusRouteForm()
        formset = StopageFormSet()
    return render(request, 'buses/custom_admin/create_route.html', {'form': form, 'formset': formset})
