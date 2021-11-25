from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.logging_view, name='logging_view'),
    path('select_logs', views.select_logs, name='select_logs'),
    path('download_schedule_csv', views.download_schedule_csv, name='download_schedule_csv'),
    path('download_climate_csv', views.download_climate_csv, name='download_climate_csv'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
