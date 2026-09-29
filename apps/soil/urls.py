from django.urls import path
from .views import guidance
app_name='soil'; urlpatterns=[path('',guidance,name='guidance')]
