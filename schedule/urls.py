from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from . import views

urlpatterns = [
    path('', views.schedule, name='schedule'),
    path('update_schedule', views.update_schedule, name='update_schedule'),
    path('remove_schedule_view', views.remove_schedule_view, name='remove_schedule_view'),
    path('relay_on_off', views.relay_on_off, name='relay_on_off'),
    # path('update_app', views.update_app, name='update_app'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
