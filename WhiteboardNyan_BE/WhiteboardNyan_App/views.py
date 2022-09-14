from django.shortcuts import render
from django.http import HttpResponse
from django.view.generic import TemplateView

# Create your views here.
def index(request):
    return HttpResponse("Hello, world!");

def WhiteboardView(TemplateView):
    template = "Whiteboard_BE/template/index.html"
