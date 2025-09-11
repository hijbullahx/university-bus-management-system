from django.contrib.auth import views as auth_views
from django.urls import path
from . import views, views_admin
from . import views_logout
from . import views_admin_route, views_admin_route_edit, views_route_stopages, views_admin_shuttle, views_admin_shuttle_edit

app_name = 'buses' # Define the app namespace

urlpatterns = [
  path('login/', auth_views.LoginView.as_view(template_name='buses/custom_admin/login.html'), name='custom_login'),
  path('logout/', views_logout.custom_logout, name='custom_logout'),
  path('', views.bus_schedule_list, name = 'bus_schedule_list'),
  path('admin-panel/', views_admin.admin_dashboard, name='custom_admin_dashboard'),
  path('admin-panel/create-route/', views_admin_route.create_route, name='custom_create_route'),
  path('admin-panel/edit-route/<int:route_id>/', views_admin_route_edit.edit_route, name='custom_edit_route'),
  path('admin-panel/delete-route/<int:route_id>/', views_admin_route_edit.delete_route, name='custom_delete_route'),
  path('route/<int:route_id>/stopages/', views_route_stopages.route_stopages_detail, name='route_stopages_detail'),
  path('admin-panel/create-shuttle-route/', views_admin_shuttle.create_shuttle_route, name='custom_create_shuttle_route'),
  path('admin-panel/edit-shuttle-route/<int:route_id>/', views_admin_shuttle_edit.edit_shuttle_route, name='custom_edit_shuttle_route'),
  path('admin-panel/delete-shuttle-route/<int:route_id>/',
       __import__('buses.views_admin_shuttle_delete').views_admin_shuttle_delete.delete_shuttle_route,
       name='custom_delete_shuttle_route'),
]