from django import forms
from .models import Recommendation
class RecommendationForm(forms.ModelForm):
    class Meta:
        model=Recommendation; fields=('nitrogen','phosphorus','potassium','ph','moisture','soil_type','temperature','humidity','rainfall','region','season','irrigation_type')
        widgets={f:forms.NumberInput(attrs={'step':'0.1','min':'0'}) for f in ('nitrogen','phosphorus','potassium','moisture','temperature','humidity','rainfall')}
