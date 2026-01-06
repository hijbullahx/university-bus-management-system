from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.dashboard, name='home'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('users/', views.user_list, name='user_list'),
    path('pending/', views.pending_registrations, name='pending_registrations'),
    path('approve/<int:pk>/', views.approve_user, name='approve_user'),
    path('reject/<int:pk>/', views.reject_user, name='reject_user'),
    # User pages
    path('home/', views.user_home, name='user_home'),
    path('live-map/', views.user_live_map, name='user_live_map'),
]
