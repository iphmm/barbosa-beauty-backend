# appointments/urls.py

from django.urls import path
from .views import ServiceListCreateView

urlpatterns = [
    # A URL para listar e criar serviços será /api/services/
    path('services/', ServiceListCreateView.as_view(), name='service-list-create'),
]