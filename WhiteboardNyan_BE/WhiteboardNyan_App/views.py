from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class WhiteboardNyanAppView(TemplateView):
    template_name = "WhiteboardNyan_App/index.html"
