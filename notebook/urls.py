from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.notebook_view, name='notebook_view'),
    path('publish_note', views.publish_note, name='publish_note'),
    path('delete_note', views.delete_note, name='delete_note'),
    path('update_notebook', views.update_notebook, name='update_notebook'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
