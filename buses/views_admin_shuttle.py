
from django.shortcuts import render, redirect
from buses.forms import ShuttleRouteForm
from buses.models import BusRoute
from buses.forms_shuttle_schedule import ShuttleScheduleFormSet

def create_shuttle_route(request):
    if request.method == 'POST':
        form = ShuttleRouteForm(request.POST)
        schedule_formset = ShuttleScheduleFormSet(request.POST)
        if form.is_valid() and schedule_formset.is_valid():
            shuttle_route = form.save(commit=False)
            shuttle_route.is_shuttle = True
            shuttle_route.save()
            # Save shuttle schedule as JSON in route.notes (or another field if you want)
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
        form = ShuttleRouteForm(initial={'is_shuttle': True})
        schedule_formset = ShuttleScheduleFormSet()
    return render(request, 'buses/custom_admin/create_shuttle_route.html', {'form': form, 'schedule_formset': schedule_formset})
