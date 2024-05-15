from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def homepage(request):
    return render(request, "appone/index.html")

def register(request):
    return render(request, "appone/register.html")