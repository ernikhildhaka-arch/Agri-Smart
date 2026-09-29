from django.conf import settings
from django.db import models

class Farm(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='farms')
    name = models.CharField(max_length=120)
    area_acres = models.DecimalField(max_digits=8, decimal_places=2)
    soil_type = models.CharField(max_length=80)
    irrigation_type = models.CharField(max_length=80)
    location = models.CharField(max_length=180)
    current_crop = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: indexes = [models.Index(fields=['owner', 'name'])]
    def __str__(self): return f'{self.name} ({self.area_acres} acres)'
