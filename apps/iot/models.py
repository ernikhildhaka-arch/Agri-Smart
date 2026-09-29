from django.db import models
from apps.land.models import Farm
class Device(models.Model):
    farm=models.ForeignKey(Farm,on_delete=models.CASCADE,related_name='devices'); device_id=models.CharField(max_length=100,unique=True); device_name=models.CharField(max_length=100); device_type=models.CharField(max_length=80); status=models.CharField(max_length=30,default='offline'); last_seen=models.DateTimeField(null=True,blank=True)
    def __str__(self): return self.device_name
class IoTReading(models.Model):
    device=models.ForeignKey(Device,on_delete=models.CASCADE,related_name='readings'); soil_moisture=models.FloatField(null=True,blank=True); water_level=models.FloatField(null=True,blank=True); temperature=models.FloatField(null=True,blank=True); humidity=models.FloatField(null=True,blank=True); simulated=models.BooleanField(default=False); timestamp=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-timestamp']; indexes=[models.Index(fields=['device','timestamp'])]
    def __str__(self): return f'{self.device} @ {self.timestamp:%Y-%m-%d %H:%M}'

class IoTAlert(models.Model):
    class Severity(models.TextChoices): LOW='low','Low'; HIGH='high','High'
    device=models.ForeignKey(Device,on_delete=models.CASCADE,related_name='alerts')
    severity=models.CharField(max_length=10,choices=Severity.choices)
    message=models.CharField(max_length=255)
    resolved=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=['-created_at']; indexes=[models.Index(fields=['device','resolved','created_at'])]
    def __str__(self): return f'{self.device}: {self.severity} water alert'
