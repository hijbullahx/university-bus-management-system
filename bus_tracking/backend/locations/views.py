from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.decorators import driver_required

@login_required
@driver_required
def share_location(request):
    """Driver location sharing page."""
    return render(request, 'locations/share_location.html')
