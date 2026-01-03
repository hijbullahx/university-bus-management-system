from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import GlobalSettings

def authority_required(view_func):
    """Decorator to check if user has AUTHORITY role"""
    return user_passes_test(lambda u: hasattr(u, 'profile') and u.profile.role == 'AUTHORITY')(view_func)

@login_required
@authority_required
def global_settings(request):
    """View for authority to manage global settings"""
    settings, created = GlobalSettings.objects.get_or_create(pk=1)  # Ensure only one instance

    if request.method == 'POST':
        active_route_type = request.POST.get('active_route_type')
        if active_route_type in dict(settings._meta.get_field('active_route_type').choices):
            settings.active_route_type = active_route_type
            settings.save()
            messages.success(request, 'Global settings updated successfully.')
        else:
            messages.error(request, 'Invalid route type selected.')
        return redirect('buses:global_settings')

    context = {
        'settings': settings,
        'route_type_choices': GlobalSettings._meta.get_field('active_route_type').choices,
    }
    return render(request, 'buses/authority/global_settings.html', context)