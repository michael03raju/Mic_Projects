from django.contrib import admin
from .models import Appointment,Doctor_details
# Register your models here.

admin.site.register(Appointment)
admin.site.register(Doctor_details)