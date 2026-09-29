from django.conf import settings
from django.db import models

class FarmerProfile(models.Model):
    class Role(models.TextChoices): FARMER = 'farmer', 'Farmer'; ADMIN = 'admin', 'Administrator'
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='farmer_profile')
    phone = models.CharField(max_length=20, blank=True)
    state = models.CharField(max_length=100, blank=True)
    district = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=80, blank=True, help_text='Optional category for scheme matching')
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.FARMER)
    def __str__(self): return f'{self.user.get_full_name() or self.user.username} profile'
