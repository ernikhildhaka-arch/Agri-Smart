import json

from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model

from apps.land.models import Farm
from .models import Device, IoTAlert


@override_settings(IOT_API_KEY='test-device-key')
class IoTIngestionTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(username='farmer', password='safe-password')
        farm = Farm.objects.create(
            owner=user, name='North field', area_acres=2, soil_type='Loam',
            irrigation_type='Drip', location='Pune', current_crop='Wheat',
        )
        self.device = Device.objects.create(
            farm=farm, device_id='esp32-north-1', device_name='North sensor', device_type='soil',
        )

    def post_reading(self, values, key='test-device-key'):
        return self.client.post(
            f'/iot/api/{self.device.device_id}/readings/',
            data=json.dumps(values),
            content_type='application/json',
            HTTP_X_IOT_API_KEY=key,
        )

    def test_ingestion_persists_reading_and_creates_low_alert(self):
        response = self.post_reading({'soil_moisture': 20, 'water_level': 50, 'temperature': 28, 'humidity': 60})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.device.readings.count(), 1)
        self.assertTrue(IoTAlert.objects.filter(device=self.device, severity='low', resolved=False).exists())

    def test_ingestion_requires_key_and_valid_ranges(self):
        self.assertEqual(self.post_reading({'soil_moisture': 20}, key='wrong').status_code, 401)
        self.assertEqual(self.post_reading({'soil_moisture': 120}).status_code, 400)
