from django.urls import path
from . import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.landing, name='landing'),
    path('dashboard/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('guide/', views.guide, name='guide'),
    path('language/toggle/', views.toggle_language, name='toggle_language'),
]
