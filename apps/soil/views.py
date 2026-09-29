from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import SoilForm
from .services import analyse
@login_required
def guidance(request):
    form=SoilForm(request.POST or None); result=None
    if request.method=='POST' and form.is_valid(): result=analyse(form.cleaned_data)
    return render(request,'soil/guidance.html',{'form':form,'result':result})
