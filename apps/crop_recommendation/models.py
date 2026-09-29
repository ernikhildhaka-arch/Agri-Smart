from django.conf import settings
from django.db import models
class Recommendation(models.Model):
    farmer=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='recommendations')
    nitrogen=models.FloatField(); phosphorus=models.FloatField(); potassium=models.FloatField(); ph=models.FloatField(); moisture=models.FloatField(); soil_type=models.CharField(max_length=60); temperature=models.FloatField(); humidity=models.FloatField(); rainfall=models.FloatField(); region=models.CharField(max_length=100); season=models.CharField(max_length=60); irrigation_type=models.CharField(max_length=60)
    crop=models.CharField(max_length=100); confidence=models.FloatField(null=True,blank=True); source=models.CharField(max_length=20,default='fallback'); created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-created_at']; indexes=[models.Index(fields=['farmer','created_at'])]
    def __str__(self): return f'{self.crop} ({self.source})'
