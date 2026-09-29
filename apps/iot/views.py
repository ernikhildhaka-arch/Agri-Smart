from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render
from .models import Device
from .services import simulated_values, ingest_reading, moisture_range_for
@login_required
def monitor(request):
    devices=Device.objects.filter(farm__owner=request.user).select_related('farm').prefetch_related('readings','alerts')
    device_cards = [{'device': device, 'range': moisture_range_for(device), 'latest': device.readings.first(), 'alerts': device.alerts.filter(resolved=False)[:3]} for device in devices]
    return render(request,'iot/monitor.html',{'device_cards':device_cards})

@login_required
def simulate(request, pk):
    if request.method != 'POST': raise Http404
    try: device = Device.objects.select_related('farm').get(pk=pk, farm__owner=request.user)
    except Device.DoesNotExist: raise Http404
    mode = request.POST.get('mode', 'normal')
    ingest_reading(device, simulated_values(device, mode), simulated=True)
    messages.success(request, f'Demo {mode} water reading generated for {device.farm.name}.')
    return redirect('iot:monitor')
