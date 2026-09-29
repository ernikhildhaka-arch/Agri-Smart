from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from .forms import ExpenseForm
from .models import Expense
class OwnerMixin(LoginRequiredMixin):
    def get_queryset(self): return Expense.objects.filter(farmer=self.request.user)
class ExpenseList(LoginRequiredMixin,ListView):
    model=Expense; template_name='expenses/list.html'; context_object_name='expenses'
    def get_queryset(self):
        qs=Expense.objects.filter(farmer=self.request.user); c=self.request.GET.get('category'); start=self.request.GET.get('start'); end=self.request.GET.get('end')
        if c: qs=qs.filter(category=c)
        if start: qs=qs.filter(date__gte=start)
        if end: qs=qs.filter(date__lte=end)
        return qs
    def get_context_data(self,**kw):
        data=super().get_context_data(**kw); base=Expense.objects.filter(farmer=self.request.user); data['total']=base.aggregate(total=Sum('amount'))['total'] or 0; data['categories']=Expense.Category.choices; data['breakdown']=base.values('category').annotate(total=Sum('amount')); return data
class ExpenseCreate(LoginRequiredMixin,CreateView):
    form_class=ExpenseForm; template_name='expenses/form.html'; success_url=reverse_lazy('expenses:list')
    def form_valid(self,form): form.instance.farmer=self.request.user; return super().form_valid(form)
class ExpenseUpdate(OwnerMixin,UpdateView): form_class=ExpenseForm; template_name='expenses/form.html'; success_url=reverse_lazy('expenses:list')
class ExpenseDelete(OwnerMixin,DeleteView): template_name='partials/confirm_delete.html'; success_url=reverse_lazy('expenses:list')
