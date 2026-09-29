from django.urls import path
from .views import overview
app_name = 'weather'
urlpatterns = [path('', overview, name='overview')]
