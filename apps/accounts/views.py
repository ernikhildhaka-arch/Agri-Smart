from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import ProfileForm, RegistrationForm
from .models import FarmerProfile

def register(request):
    if request.user.is_authenticated: return redirect('dashboard:home')
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(); FarmerProfile.objects.create(user=user); login(request, user); return redirect('dashboard:home')
    return render(request, 'accounts/register.html', {'form': form})
@login_required
def profile(request):
    profile, _ = FarmerProfile.objects.get_or_create(user=request.user)
    form = ProfileForm(request.POST or None, instance=profile)
    if request.method == 'POST' and form.is_valid(): form.save(); return redirect('accounts:profile')
    return render(request, 'accounts/profile.html', {'form': form})
