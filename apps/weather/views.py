from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.land.models import Farm
from .services import get_weather

@login_required
def overview(request):
    farm = Farm.objects.filter(owner=request.user).first()
    location = request.GET.get('location') or (farm.location if farm else getattr(getattr(request.user, 'farmer_profile', None), 'district', ''))
    return render(request, 'weather/overview.html', {'weather': get_weather(location), 'farm': farm})
