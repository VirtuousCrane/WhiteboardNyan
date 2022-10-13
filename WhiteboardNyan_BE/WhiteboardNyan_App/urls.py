from django.urls import path

from . import views

app_name = 'WhiteboardNyan_BE.WhiteboardNyan_App'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('sample/', views.SampleView.as_view(), name='detail'),
]