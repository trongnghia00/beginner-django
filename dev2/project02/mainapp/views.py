from django.shortcuts import render, redirect

from .forms import CreateUserForm, LoginForm, ThoughtForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages

# Create your views here.

def homepage(request):
    return render(request, "mainapp/index.html")

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tài khoản được tạo thành công !")
            return redirect('login')
    context = {'form': form}
    return render(request, "mainapp/register.html", context)

def my_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    
    context = {'form': form}
    return render(request, "mainapp/my-login.html", context)

def user_logout(request):
    logout(request)
    return redirect('')

@login_required(login_url='login')
def dashboard(request):
    return render(request, "mainapp/dashboard.html")

@login_required(login_url='login')
def create_thought(request):
    form = ThoughtForm()
    if request.method == 'POST':
        form = ThoughtForm(request.POST)
        if form.is_valid():
            thought = form.save(commit=False)
            thought.user = request.user
            thought.save()
            return redirect('dashboard')
        
    context = {'form' : form}

    return render(request, 'mainapp/create-thought.html', context)
