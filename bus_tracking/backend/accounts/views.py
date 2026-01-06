from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import LoginForm, UserRegistrationForm, UserProfileForm
from .models import User
from buses.models import Bus, BusAssignment
from schedules.models import Route, Schedule
from issues.models import Issue
from notifications.models import Notification

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('accounts:dashboard')


class CustomLogoutView(LogoutView):
    next_page = 'accounts:login'


class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        # The form's save() method handles setting approval_status, is_active, and password
        form.save()
        messages.success(self.request, 'Registration submitted! Please wait for admin approval. You can login using your username and University ID.')
        return redirect(self.success_url)


@login_required
def dashboard(request):
    user = request.user
    context = {'user': user}

    if user.is_regular_user:
        context['buses'] = Bus.objects.filter(is_active=True)[:5]
        context['routes'] = Route.objects.filter(is_active=True)[:5]
        context['notifications'] = Notification.objects.filter(
            is_active=True
        ).order_by('-created_at')[:5]
        return render(request, 'accounts/dashboard_user.html', context)

    elif user.is_driver:
        try:
            assignment = BusAssignment.objects.select_related('bus', 'route').get(
                driver=user, is_active=True
            )
            context['assignment'] = assignment
            context['bus'] = assignment.bus
            context['route'] = assignment.route
        except BusAssignment.DoesNotExist:
            context['assignment'] = None
        
        context['recent_issues'] = Issue.objects.filter(
            reported_by=user
        ).order_by('-created_at')[:5]
        return render(request, 'accounts/dashboard_driver.html', context)

    elif user.is_admin_user:
        context['total_buses'] = Bus.objects.count()
        context['active_buses'] = Bus.objects.filter(is_active=True).count()
        context['total_routes'] = Route.objects.count()
        context['total_drivers'] = User.objects.filter(role='driver').count()
        context['pending_issues'] = Issue.objects.filter(status='pending').count()
        context['pending_registrations'] = User.objects.filter(approval_status='pending').count()
        context['recent_issues'] = Issue.objects.order_by('-created_at')[:5]
        return render(request, 'accounts/dashboard_admin.html', context)

    elif user.is_authority:
        context['total_buses'] = Bus.objects.count()
        context['active_buses'] = Bus.objects.filter(is_active=True).count()
        context['total_routes'] = Route.objects.count()
        context['total_users'] = User.objects.filter(role__in=['student', 'faculty', 'staff']).count()
        context['total_drivers'] = User.objects.filter(role='driver').count()
        return render(request, 'accounts/dashboard_authority.html', context)

    return render(request, 'accounts/dashboard_user.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def user_list(request):
    if not request.user.is_admin_user and not request.user.is_authority:
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    users = User.objects.all().order_by('-created_at')
    return render(request, 'accounts/user_list.html', {'users': users})


@login_required
def pending_registrations(request):
    """Admin view for pending user registrations"""
    if not request.user.is_admin_user:
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    pending_users = User.objects.filter(approval_status='pending').order_by('-created_at')
    return render(request, 'accounts/pending_registrations.html', {'pending_users': pending_users})


@login_required
def approve_user(request, pk):
    """Approve a pending user registration"""
    if not request.user.is_admin_user:
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    user = get_object_or_404(User, pk=pk, approval_status='pending')
    
    if request.method == 'POST':
        from django.utils import timezone
        user.approval_status = 'approved'
        user.approved_by = request.user
        user.approved_at = timezone.now()
        user.is_active = True
        user.save()
        messages.success(request, f'User {user.username} has been approved.')
        return redirect('accounts:pending_registrations')
    
    return render(request, 'accounts/approve_user.html', {'pending_user': user})


@login_required
def reject_user(request, pk):
    """Reject a pending user registration"""
    if not request.user.is_admin_user:
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    user = get_object_or_404(User, pk=pk, approval_status='pending')
    
    if request.method == 'POST':
        user.approval_status = 'rejected'
        user.rejection_reason = request.POST.get('reason', '')
        user.is_active = False
        user.save()
        messages.success(request, f'User {user.username} has been rejected.')
        return redirect('accounts:pending_registrations')
    
    return render(request, 'accounts/reject_user.html', {'pending_user': user})


@login_required
def user_home(request):
    """Home page for regular users (students, faculty, staff)"""
    from notifications.models import Notification
    
    context = {
        'user': request.user,
        'routes': Route.objects.filter(is_active=True, is_published=True).prefetch_related('stops', 'trips')[:6],
        'announcements': Notification.objects.filter(
            notification_type='general',
            is_active=True
        ).order_by('-created_at')[:5],
    }
    return render(request, 'accounts/user_home.html', context)


@login_required
def user_live_map(request):
    """Live map page for regular users"""
    context = {
        'routes': Route.objects.filter(is_active=True, is_published=True),
        'buses': Bus.objects.filter(is_active=True).select_related('current_route'),
    }
    return render(request, 'accounts/user_live_map.html', context)

