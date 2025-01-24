from django.urls import path
from views import *
urlpatterns = [
    path('', index, name='index'),
    path('video/', test, name='test'),
    path('video_feed_yolo/', video_feed_yolo, name='video_feed_yolo'),
    path("analysis/", analysis, name="analysis"),
]
