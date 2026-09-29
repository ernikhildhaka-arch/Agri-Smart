from django import forms
class ProfitForm(forms.Form):
    crop=forms.CharField(max_length=100); land_area=forms.FloatField(min_value=0.01); yield_amount=forms.FloatField(min_value=0); seed_cost=forms.FloatField(min_value=0); fertilizer_cost=forms.FloatField(min_value=0); pesticide_cost=forms.FloatField(min_value=0); labour_cost=forms.FloatField(min_value=0); irrigation_cost=forms.FloatField(min_value=0); other_cost=forms.FloatField(min_value=0); market_price=forms.FloatField(min_value=0,label='Expected market price per yield unit')
