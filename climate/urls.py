from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from .views import climate, set_climate

urlpatterns = [
    path('', climate, name='climate_view'),
    path('set_climate', set_climate, name='set_climate'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
