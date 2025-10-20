# appointments/serializers.py

from rest_framework import serializers
from .models import Service, Appointment, Address
from django.contrib.auth.models import User

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'price', 'duration_minutes', 'image']