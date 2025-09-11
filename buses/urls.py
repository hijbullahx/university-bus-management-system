from django.urls import path
from . import views, views_admin
from . import views_logout
from . import views_admin_route, views_admin_route_edit

app_name = 'buses' # Define the app namespace

urlpatterns = [
  path('logout/', views_logout.custom_logout, name='custom_logout'),
  path('', views.bus_schedule_list, name = 'bus_schedule_list'),
  path('admin-panel/', views_admin.admin_dashboard, name='custom_admin_dashboard'),
  path('admin-panel/create-route/', views_admin_route.create_route, name='custom_create_route'),
  path('admin-panel/edit-route/<int:route_id>/', views_admin_route_edit.edit_route, name='custom_edit_route'),
  path('admin-panel/delete-route/<int:route_id>/', views_admin_route_edit.delete_route, name='custom_delete_route'),
]