from django.urls import path
from .views import predict
app_name='profit'; urlpatterns=[path('',predict,name='predict')]
