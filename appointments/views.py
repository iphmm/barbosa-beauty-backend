# appointments/views.py

from rest_framework import generics
from .models import Service
from .serializers import ServiceSerializer

class ServiceListCreateView(generics.ListCreateAPIView):
    """
    Esta view permite:
    - Listar todos os serviços (GET)
    - Criar um novo serviço (POST) - (Isso será mais útil com o front-end)
    """
    queryset = Service.objects.all().order_by('name') # Busca todos os serviços no banco
    serializer_class = ServiceSerializer              # Diz como traduzir os dados para JSON