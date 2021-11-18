from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from .views import climate, set_climate, download_climate_csv, select_climate_logs

urlpatterns = [
    path('', climate, name='climate_view'),
    path('set_climate', set_climate, name='set_climate'),
    path('select_climate_logs', select_climate_logs, name='select_climate_logs'),
    path('download_climate_csv', download_climate_csv, name='download_climate_csv'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
