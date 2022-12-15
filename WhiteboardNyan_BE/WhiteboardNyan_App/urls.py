from django.urls import path
from django.conf.urls import url

from . import views
from .consumers import WhiteboardConsumer

app_name = 'WhiteboardNyan_BE.WhiteboardNyan_App'
urlpatterns = [
    path('whiteboard/<room_code>', views.IndexView.as_view(), name='index'),
    path('', views.SplashView.as_view(), name='splash'),
    path('sample/', views.SampleView.as_view(), name='detail'),
]
