from django.views.generic import TemplateView

# Create your views here.
class IndexView(TemplateView):
    template_name = "WhiteboardNyan_App/index.html"

class SplashView(TemplateView):
    template_name = "WhiteboardNyan_App/splash.html"

class SampleView(TemplateView):
    template_name = "WhiteboardNyan_App/sample.html"
