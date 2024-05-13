from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def homepage(request):
    return HttpResponse("This is the homepage.")

def register(request):
    return HttpResponse("This is registration page.")