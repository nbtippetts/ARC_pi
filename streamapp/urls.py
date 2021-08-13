from django.urls import path, include
from streamapp import views


urlpatterns = [
    path('', views.index, name='video_view'),
    path('video_feed', views.video_feed, name='video_feed'),
    # path('capture_frame', views.capture_frame, name='capture_frame'),
    ]
