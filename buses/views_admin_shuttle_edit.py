
from django.shortcuts import render, redirect, get_object_or_404
from buses.forms import ShuttleRouteForm
from buses.models import BusRoute
from buses.forms_shuttle_schedule import ShuttleScheduleFormSet
import ast

def edit_shuttle_route(request, route_id):
    shuttle_route = get_object_or_404(BusRoute, pk=route_id, is_shuttle=True)
    # Load existing schedule data (no notes field, so use empty or implement another storage)
    initial_data = []
    if request.method == 'POST':
        form = ShuttleRouteForm(request.POST, instance=shuttle_route)
        schedule_formset = ShuttleScheduleFormSet(request.POST)
        if form.is_valid() and schedule_formset.is_valid():
            form.save()
            # Here you would save the schedule data somewhere appropriate
            # For now, just ignore saving schedule data since there is no notes field
            return redirect('buses:custom_admin_dashboard')
    else:
        form = ShuttleRouteForm(instance=shuttle_route)
        schedule_formset = ShuttleScheduleFormSet(initial=initial_data)
    return render(request, 'buses/custom_admin/edit_shuttle_route.html', {'form': form, 'schedule_formset': schedule_formset, 'route': shuttle_route})
