from django import forms
class SoilForm(forms.Form):
    nitrogen=forms.FloatField(min_value=0); phosphorus=forms.FloatField(min_value=0); potassium=forms.FloatField(min_value=0); ph=forms.FloatField(min_value=0,max_value=14); moisture=forms.FloatField(min_value=0,max_value=100); soil_type=forms.CharField(max_length=60)
