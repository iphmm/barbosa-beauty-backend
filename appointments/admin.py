from django.contrib import admin
from .models import Service, Address, Appointment

admin.site.register(Service)
admin.site.register(Address)
admin.site.register(Appointment)