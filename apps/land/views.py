from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from .forms import FarmForm
from .models import Farm
class OwnerQuerysetMixin(LoginRequiredMixin):
    def get_queryset(self): return Farm.objects.filter(owner=self.request.user)
class FarmListView(LoginRequiredMixin, ListView):
    model = Farm; template_name = 'land/list.html'; context_object_name = 'farms'
    def get_queryset(self): return Farm.objects.filter(owner=self.request.user)
class FarmCreateView(LoginRequiredMixin, CreateView):
    form_class = FarmForm; template_name = 'land/form.html'; success_url = reverse_lazy('land:list')
    def form_valid(self, form): form.instance.owner = self.request.user; return super().form_valid(form)
class FarmUpdateView(OwnerQuerysetMixin, UpdateView): form_class = FarmForm; template_name = 'land/form.html'; success_url = reverse_lazy('land:list')
class FarmDeleteView(OwnerQuerysetMixin, DeleteView): template_name = 'partials/confirm_delete.html'; success_url = reverse_lazy('land:list')
