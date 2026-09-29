from django import forms
from .models import Farm
class FarmForm(forms.ModelForm):
    class Meta:
        model = Farm; fields = ('name', 'area_acres', 'soil_type', 'irrigation_type', 'location', 'current_crop')
        widgets = {'area_acres': forms.NumberInput(attrs={'min': '0.01', 'step': '0.01'})}
