from django.db import models
class Scheme(models.Model):
    name=models.CharField(max_length=180); description=models.TextField(); state=models.CharField(max_length=100,blank=True,help_text='Leave blank for all-India schemes'); eligibility=models.TextField(); benefits=models.TextField(); official_url=models.URLField(blank=True); category=models.CharField(max_length=80,blank=True); min_land_acres=models.DecimalField(max_digits=8,decimal_places=2,null=True,blank=True); crop=models.CharField(max_length=100,blank=True); verified_at=models.DateField(null=True,blank=True)
    class Meta: indexes=[models.Index(fields=['state','category'])]
    def __str__(self): return self.name
