from django.utils import timezone
from .models import IoTAlert, IoTReading

# Helper to format alert messages (optional for future use)
def alert_message(reading, lower, upper):
    """Return a user‑friendly alert message based on the soil moisture reading.

    Args:
        reading: IoTReading instance containing ``soil_moisture``.
        lower (int): Lower bound of the target moisture range.
        upper (int): Upper bound of the target moisture range.
    """
    crop = reading.device.farm.current_crop or 'this crop'
    moisture = reading.soil_moisture
    if moisture < lower:
        return f'Low water: {crop} is at {moisture}% moisture; target range is {lower}–{upper}%.'
    elif moisture > upper:
        return f'High water: {crop} is at {moisture}% moisture; target range is {lower}–{upper}%. Check drainage and pause irrigation.'
    return None

CROP_MOISTURE_RANGES = {
    'rice': (60, 85), 'paddy': (60, 85), 'wheat': (35, 55), 'maize': (40, 60),
    'corn': (40, 60), 'potato': (45, 65), 'sugarcane': (55, 75), 'cotton': (40, 60),
}

def moisture_range_for(farm):
    crop = (farm.current_crop or '').lower()
    return next((limits for name, limits in CROP_MOISTURE_RANGES.items() if name in crop), (35, 60))

def evaluate_water_status(reading):
    if reading.soil_moisture is None:
        return None
    lower, upper = moisture_range_for(reading.device.farm)
    # Use helper to generate a clear message
    message = alert_message(reading, lower, upper)
    if message is None:
        # No alert – clear any existing unresolved alerts for this device
        IoTAlert.objects.filter(device=reading.device, resolved=False).update(resolved=True)
        return None
    # Determine severity based on moisture direction
    severity = IoTAlert.Severity.LOW if reading.soil_moisture < lower else IoTAlert.Severity.HIGH
    alert, _ = IoTAlert.objects.get_or_create(
        device=reading.device,
        severity=severity,
        message=message,
        resolved=False,
    )
    return alert

def ingest_reading(device, values, simulated=False):
    reading=IoTReading.objects.create(device=device,simulated=simulated,**values); device.last_seen=timezone.now(); device.status='demo' if simulated else 'online'; device.save(update_fields=['last_seen','status']); evaluate_water_status(reading); return reading

def simulated_values(device, mode='normal'):
    lower, upper = moisture_range_for(device.farm)
    moisture = lower - 8 if mode == 'low' else upper + 8 if mode == 'high' else round((lower + upper) / 2)
    return {'soil_moisture': moisture, 'water_level': 50, 'temperature': 28, 'humidity': 62}
