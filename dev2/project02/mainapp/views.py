from django.shortcuts import render, redirect

from .forms import CreateUserForm

# Create your views here.

def homepage(request):
    return render(request, "mainapp/index.html")

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form': form}
    return render(request, "mainapp/register.html", context)

def my_login(request):
    return render(request, "mainapp/my-login.html")

def dashboard(request):
    return render(request, "mainapp/dashboard.html")