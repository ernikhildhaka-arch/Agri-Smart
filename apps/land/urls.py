from django.urls import path
from .views import *
app_name='land'
urlpatterns=[path('', FarmListView.as_view(), name='list'), path('add/', FarmCreateView.as_view(), name='add'), path('<int:pk>/edit/', FarmUpdateView.as_view(), name='edit'), path('<int:pk>/delete/', FarmDeleteView.as_view(), name='delete')]
