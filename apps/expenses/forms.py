from django import forms
from .models import Expense
class ExpenseForm(forms.ModelForm):
    class Meta: model=Expense; fields=('category','amount','date','note'); widgets={'date':forms.DateInput(attrs={'type':'date'}),'amount':forms.NumberInput(attrs={'min':'0.01','step':'0.01'})}
