from django.shortcuts import render, redirect, get_object_or_404
from buses.models import BusRoute

def delete_shuttle_route(request, route_id):
    route = get_object_or_404(BusRoute, pk=route_id, is_shuttle=True)
    if request.method == 'POST':
        route.delete()
        return redirect('buses:custom_admin_dashboard')
    return render(request, 'buses/custom_admin/delete_route.html', {'route': route})
