from django.conf import settings
from django.db import models
class Expense(models.Model):
    class Category(models.TextChoices):
        SEEDS='seeds','Seeds'; FERTILIZER='fertilizer','Fertilizer'; PESTICIDES='pesticides','Pesticides'; LABOUR='labour','Labour'; IRRIGATION='irrigation','Irrigation'; MACHINERY='machinery','Machinery'; TRANSPORT='transport','Transport'; OTHER='other','Other'
    farmer=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='expenses'); category=models.CharField(max_length=20,choices=Category.choices); amount=models.DecimalField(max_digits=12,decimal_places=2); date=models.DateField(); note=models.CharField(max_length=240,blank=True)
    class Meta: ordering=['-date']; indexes=[models.Index(fields=['farmer','date']),models.Index(fields=['farmer','category'])]
    def __str__(self): return f'{self.get_category_display()} - ₹{self.amount}'
