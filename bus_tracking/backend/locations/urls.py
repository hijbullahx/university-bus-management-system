from django.urls import path
from . import views

app_name = 'locations'

urlpatterns = [
    path('share/', views.share_location, name='share_location'),
]
