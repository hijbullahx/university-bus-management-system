from django.shortcuts import render, get_object_or_404
from .models import BusRoute, Stopage

def route_stopages_detail(request, route_id):
    route = get_object_or_404(BusRoute, pk=route_id)
    stopages = route.stopages.order_by('pickup_time').all()
    return render(request, 'route_stopages_detail.html', {
        'route': route,
        'stopages': stopages,
    })
