from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def homepage(request):
    data = {'name': 'Nghia'}
    return render(request, "appone/index.html", data)

def register(request):
    return render(request, "appone/register.html")