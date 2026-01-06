from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from accounts.decorators import admin_required
from .models import Bus, BusAssignment
from .forms import BusForm, BusAssignmentForm

@login_required
def bus_list(request):
    buses = Bus.objects.select_related('current_route').all()
    
    status = request.GET.get('status')
    if status == 'active':
        buses = buses.filter(is_active=True)
    elif status == 'inactive':
        buses = buses.filter(is_active=False)
    
    paginator = Paginator(buses, 12)
    page = request.GET.get('page')
    buses = paginator.get_page(page)
    
    return render(request, 'buses/bus_list.html', {'buses': buses})


@login_required
def bus_detail(request, pk):
    bus = get_object_or_404(Bus.objects.select_related('current_route'), pk=pk)
    locations = bus.locations.order_by('-timestamp')[:10]
    assignments = bus.assignments.select_related('driver', 'route').order_by('-date')[:5]
    
    return render(request, 'buses/bus_detail.html', {
        'bus': bus,
        'locations': locations,
        'assignments': assignments
    })


@login_required
@admin_required
def bus_create(request):
    if request.method == 'POST':
        form = BusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bus created successfully.')
            return redirect('buses:bus_list')
    else:
        form = BusForm()
    
    return render(request, 'buses/bus_form.html', {'form': form, 'title': 'Add New Bus'})


@login_required
@admin_required
def bus_edit(request, pk):
    bus = get_object_or_404(Bus, pk=pk)
    
    if request.method == 'POST':
        form = BusForm(request.POST, instance=bus)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bus updated successfully.')
            return redirect('buses:bus_detail', pk=pk)
    else:
        form = BusForm(instance=bus)
    
    return render(request, 'buses/bus_form.html', {'form': form, 'title': 'Edit Bus', 'bus': bus})


@login_required
@admin_required
def bus_delete(request, pk):
    bus = get_object_or_404(Bus, pk=pk)
    
    if request.method == 'POST':
        bus.delete()
        messages.success(request, 'Bus deleted successfully.')
        return redirect('buses:bus_list')
    
    return render(request, 'buses/bus_confirm_delete.html', {'bus': bus})


@login_required
def live_map(request):
    return render(request, 'buses/live_map.html')


@login_required
def follow_bus(request, pk):
    bus = get_object_or_404(Bus, pk=pk)
    return render(request, 'buses/follow_bus.html', {'bus': bus})


@login_required
@admin_required
def assignment_list(request):
    assignments = BusAssignment.objects.select_related('bus', 'driver', 'route').order_by('-date')
    paginator = Paginator(assignments, 20)
    page = request.GET.get('page')
    assignments = paginator.get_page(page)
    
    return render(request, 'buses/assignment_list.html', {'assignments': assignments})


@login_required
@admin_required
def assignment_create(request):
    if request.method == 'POST':
        form = BusAssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Assignment created successfully.')
            return redirect('buses:assignment_list')
    else:
        form = BusAssignmentForm()
    
    return render(request, 'buses/assignment_form.html', {'form': form, 'title': 'Create Assignment'})
