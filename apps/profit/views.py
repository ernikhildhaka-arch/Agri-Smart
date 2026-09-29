from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import ProfitForm
from .services import calculate
@login_required
def predict(request):
    form=ProfitForm(request.POST or None); result=None
    if request.method=='POST' and form.is_valid(): result=calculate(form.cleaned_data)
    return render(request,'profit/predict.html',{'form':form,'result':result})
