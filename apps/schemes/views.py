from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Scheme
@login_required
def list_schemes(request):
    profile=getattr(request.user,'farmer_profile',None); state=request.GET.get('state') or (profile.state if profile else ''); qs=Scheme.objects.all()
    if state: qs=qs.filter(state__iexact=state) | qs.filter(state='')
    return render(request,'schemes/list.html',{'schemes':qs.distinct(),'state':state,'profile':profile})
