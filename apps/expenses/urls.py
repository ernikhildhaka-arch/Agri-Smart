from django.urls import path
from .views import *
app_name='expenses'; urlpatterns=[path('',ExpenseList.as_view(),name='list'),path('add/',ExpenseCreate.as_view(),name='add'),path('<int:pk>/edit/',ExpenseUpdate.as_view(),name='edit'),path('<int:pk>/delete/',ExpenseDelete.as_view(),name='delete')]
