from django.urls import path
from .views import list_schemes
app_name='schemes'; urlpatterns=[path('',list_schemes,name='list')]
