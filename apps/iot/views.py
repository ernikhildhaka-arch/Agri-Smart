import json
import math
import secrets

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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


@csrf_exempt
def ingest(request, device_id):
    """Accept one sensor reading from a device gateway and persist its alert state."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    configured_key = getattr(settings, 'IOT_API_KEY', '')
    supplied_key = request.headers.get('X-IOT-API-KEY', '')
    if not configured_key or not secrets.compare_digest(supplied_key, configured_key):
        return JsonResponse({'error': 'invalid device credentials'}, status=401)
    try:
        values = json.loads(request.body.decode('utf-8'))
        values = {field: values[field] for field in (
            'soil_moisture', 'water_level', 'temperature', 'humidity'
        ) if field in values}
        if not values:
            raise ValueError('at least one reading is required')
        for field, value in values.items():
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                raise ValueError(f'{field} must be numeric')
            if not math.isfinite(value):
                raise ValueError(f'{field} must be finite')
            if field in ('soil_moisture', 'water_level', 'humidity') and not 0 <= value <= 100:
                raise ValueError(f'{field} must be between 0 and 100')
            if field == 'temperature' and not -50 <= value <= 70:
                raise ValueError('temperature must be between -50 and 70')
        device = Device.objects.select_related('farm').get(device_id=device_id)
    except (json.JSONDecodeError, UnicodeDecodeError, ValueError) as error:
        return JsonResponse({'error': str(error)}, status=400)
    except Device.DoesNotExist:
        return JsonResponse({'error': 'device not found'}, status=404)
    reading = ingest_reading(device, values)
    alert = device.alerts.filter(resolved=False).first()
    return JsonResponse({
        'id': reading.id,
        'device_id': device.device_id,
        'timestamp': reading.timestamp.isoformat(),
        'alert': alert.message if alert else None,
    }, status=201)
