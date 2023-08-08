from django.shortcuts import render # here by default 

from django.http import HttpResponse # new 

from django.views.generic import TemplateView 

# Create your views here. 

def homePageView(request): # new 

    return HttpResponse('Hello World!') # new 

class HomePageView(TemplateView): 

    template_name = "pages/home.html"