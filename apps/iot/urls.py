from django.urls import path
from .views import monitor, simulate
app_name='iot'; urlpatterns=[path('',monitor,name='monitor'), path('<int:pk>/simulate/', simulate, name='simulate')]
