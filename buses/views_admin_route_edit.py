from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import BusRoute, Stopage
from .forms import BusRouteForm, StopageFormSet
from .views_admin import staff_required
from django.shortcuts import render, redirect

@login_required
@staff_required
def edit_route(request, route_id):
    route = get_object_or_404(BusRoute, pk=route_id)
    if request.method == 'POST':
        form = BusRouteForm(request.POST, instance=route)
        formset = StopageFormSet(request.POST, instance=route)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('buses:custom_admin_dashboard')
    else:
        form = BusRouteForm(instance=route)
        formset = StopageFormSet(instance=route)
    return render(request, 'buses/custom_admin/edit_route.html', {'form': form, 'formset': formset, 'route': route})

@login_required
@staff_required
def delete_route(request, route_id):
    route = get_object_or_404(BusRoute, pk=route_id)
    if request.method == 'POST':
        route.delete()
        return redirect('buses:custom_admin_dashboard')
    return render(request, 'buses/custom_admin/delete_route.html', {'route': route})
