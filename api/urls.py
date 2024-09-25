# netbox/auto_ip_alloc/api/urls.py

from django.urls import path
from .views import AllocateIPView

app_name = 'auto_ip_alloc'

urlpatterns = [
    path('allocate-ip/', AllocateIPView.as_view(), name='allocate_ip'),
]
