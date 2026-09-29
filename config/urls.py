from django.contrib import admin
from django.urls import include, path

urlpatterns = [path('admin/', admin.site.urls), path('', include('apps.dashboard.urls')), path('accounts/', include('apps.accounts.urls')), path('farm/', include('apps.land.urls')), path('crops/', include('apps.crop_recommendation.urls')), path('soil/', include('apps.soil.urls')), path('profit/', include('apps.profit.urls')), path('expenses/', include('apps.expenses.urls')), path('schemes/', include('apps.schemes.urls')), path('assistant/', include('apps.chatbot.urls')), path('iot/', include('apps.iot.urls')), path('weather/', include('apps.weather.urls'))]
