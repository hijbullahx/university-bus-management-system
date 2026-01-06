from django.urls import path
from . import api_views

urlpatterns = [
    path('issues/', api_views.issue_list_api, name='api_issue_list'),
    path('issues/create/', api_views.issue_create_api, name='api_issue_create'),
    path('issues/<int:pk>/', api_views.issue_detail_api, name='api_issue_detail'),
    path('issues/<int:pk>/update/', api_views.issue_update_api, name='api_issue_update'),
]
