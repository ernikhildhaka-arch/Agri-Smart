from django.urls import path
from .views import ingest, monitor, simulate
app_name='iot'; urlpatterns=[path('',monitor,name='monitor'), path('api/<str:device_id>/readings/', ingest, name='ingest'), path('<int:pk>/simulate/', simulate, name='simulate')]
