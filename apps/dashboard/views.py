from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth
import json
from django.contrib import messages
from django.shortcuts import redirect, render
from apps.expenses.models import Expense
from apps.land.models import Farm
from apps.crop_recommendation.models import Recommendation
from .forms import ContactForm

def landing(request):
    return render(request, 'public/landing.html')

def toggle_language(request):
    request.session['site_language'] = 'en' if request.session.get('site_language') == 'hi' else 'hi'
    return redirect(request.POST.get('next') or request.META.get('HTTP_REFERER') or 'dashboard:landing')

def about(request):
    return render(request, 'public/about.html')

def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Thank you — your message has been received.')
        return redirect('dashboard:contact')
    return render(request, 'public/contact.html', {'form': form})

def privacy(request):
    return render(request, 'public/legal.html', {'page_title': 'Privacy Policy', 'sections': [('What we collect', 'We collect only the account, farm, and planning information you choose to enter.'), ('How we use it', 'Your information is used to operate your personal farm workspace and improve your requests.'), ('Your control', 'You can update your profile and remove private farm records from your workspace.')]})

def terms(request):
    return render(request, 'public/legal.html', {'page_title': 'Terms & Conditions', 'sections': [('Informational service', 'Recommendations and estimates are decision-support information, not a replacement for advice from local agricultural experts.'), ('Your responsibility', 'You are responsible for validating field inputs and decisions before acting on them.'), ('Availability', 'Features that rely on models, providers, schemes, or devices may be unavailable or operate in clearly marked development mode.')]})

def guide(request):
    return render(request, 'public/guide.html')

@login_required
def home(request):
    farms=Farm.objects.filter(owner=request.user); expenses=Expense.objects.filter(farmer=request.user); recent=expenses[:5]; latest=Recommendation.objects.filter(farmer=request.user).first()
    category_rows = expenses.values('category').annotate(total=Sum('amount')).order_by('category')
    month_rows = expenses.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('amount')).order_by('month')
    chart_data = {'category': {'labels': [row['category'].title() for row in category_rows], 'values': [float(row['total']) for row in category_rows]}, 'monthly': {'labels': [row['month'].strftime('%b %Y') for row in month_rows], 'values': [float(row['total']) for row in month_rows]}}
    return render(request,'dashboard/home.html',{'farm_count':farms.count(),'land_area':farms.aggregate(v=Sum('area_acres'))['v'] or 0,'recent_expenses':recent,'expense_total':expenses.aggregate(v=Sum('amount'))['v'] or 0,'latest':latest,'season':'Kharif / Rabi — set recommendations per local conditions','chart_data':json.dumps(chart_data)})
