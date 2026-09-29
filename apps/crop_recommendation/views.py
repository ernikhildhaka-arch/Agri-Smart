from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect,render
from .forms import RecommendationForm
from .services import recommend
@login_required
def create(request):
    form=RecommendationForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        features=form.cleaned_data; outcome=recommend(features); item=form.save(commit=False); item.farmer=request.user; item.crop=outcome['crop']; item.confidence=outcome['confidence']; item.source=outcome['source']; item.save(); return render(request,'crop_recommendation/result.html',{'recommendation':item,'outcome':outcome,'inputs':features.items()})
    return render(request,'crop_recommendation/form.html',{'form':form})
