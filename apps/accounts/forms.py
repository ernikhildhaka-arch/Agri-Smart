from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import FarmerProfile

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=150); last_name = forms.CharField(max_length=150, required=False); email = forms.EmailField()
    class Meta: model = User; fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
class ProfileForm(forms.ModelForm):
    class Meta: model = FarmerProfile; fields = ('phone', 'state', 'district', 'category')
