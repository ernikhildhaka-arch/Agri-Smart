from django.contrib import admin
from .models import Device, IoTAlert, IoTReading
admin.site.register(Device); admin.site.register(IoTReading); admin.site.register(IoTAlert)
