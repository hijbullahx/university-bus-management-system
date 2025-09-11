
from django.shortcuts import render, redirect, get_object_or_404
from buses.forms import ShuttleRouteForm
from buses.models import BusRoute
from buses.forms_shuttle_schedule import ShuttleScheduleFormSet
import ast

def edit_shuttle_route(request, route_id):
    shuttle_route = get_object_or_404(BusRoute, pk=route_id, is_shuttle=True)
    import ast
    # Load existing schedule data from notes field (if present)
    initial_data = []
    if shuttle_route.notes:
        try:
            initial_data = ast.literal_eval(shuttle_route.notes)
            # Convert string times to Python time objects for formset
            from datetime import datetime
            for item in initial_data:
                if 'campus_departure' in item:
                    item['campus_departure'] = datetime.strptime(item['campus_departure'], '%H:%M').time()
                if 'center_station_departure' in item:
                    item['center_station_departure'] = datetime.strptime(item['center_station_departure'], '%H:%M').time()
        except Exception:
            initial_data = []
    if request.method == 'POST':
        form = ShuttleRouteForm(request.POST, instance=shuttle_route)
        schedule_formset = ShuttleScheduleFormSet(request.POST)
        if form.is_valid() and schedule_formset.is_valid():
            form.save()
            # Save shuttle schedule as JSON in notes field
            schedule_data = []
            for schedule_form in schedule_formset:
                if schedule_form.cleaned_data and not schedule_form.cleaned_data.get('DELETE', False):
                    schedule_data.append({
                        'campus_departure': schedule_form.cleaned_data['campus_departure'].strftime('%H:%M'),
                        'center_station_departure': schedule_form.cleaned_data['center_station_departure'].strftime('%H:%M'),
                    })
            shuttle_route.notes = str(schedule_data)
            shuttle_route.save()
            return redirect('buses:custom_admin_dashboard')
    else:
        form = ShuttleRouteForm(instance=shuttle_route)
        schedule_formset = ShuttleScheduleFormSet(initial=initial_data)
    return render(request, 'buses/custom_admin/edit_shuttle_route.html', {'form': form, 'schedule_formset': schedule_formset, 'route': shuttle_route})
