from django.shortcuts import render

# Create your views here.

def homepage(request):
    return render(request, "mainapp/index.html")

def register(request):
    return render(request, "mainapp/register.html")

def my_login(request):
    return render(request, "mainapp/my-login.html")

def dashboard(request):
    return render(request, "mainapp/dashboard.html")