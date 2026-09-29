from django.urls import path
from .views import create
app_name='crop'; urlpatterns=[path('',create,name='create')]
