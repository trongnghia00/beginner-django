from django.shortcuts import render, redirect

from .forms import CreateUserForm, LoginForm, ThoughtForm, UpdateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .models import Thought
from django.contrib.auth.models import User

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

@login_required(login_url='login')
def my_thoughts(request):
    current_user = request.user.id # Lấy id của user hiện hành
    thoughts = Thought.objects.all().filter(user=current_user)

    context = {'Thoughts': thoughts}
    return render(request, "mainapp/my-thoughts.html", context)

@login_required(login_url='login')
def update_thought(request, id):
    try:
        thought = Thought.objects.get(id=id, user=request.user)
    except:
        return redirect("my-thoughts")
    
    form = ThoughtForm(instance=thought)

    if request.method == 'POST':
        form = ThoughtForm(request.POST, instance=thought)
        if form.is_valid():
            form.save()
            return redirect('my-thoughts')
        
    context = {'form': form}

    return render(request, "mainapp/update-thought.html", context)

@login_required(login_url='login')
def delete_thought(request, id):
    try:
        thought = Thought.objects.get(id=id, user=request.user)
    except:
        return redirect("my-thoughts")

    if request.method == 'POST' :
        thought.delete()
        return redirect('my-thoughts')
    
    context = {'thought': thought}
    return render(request, "mainapp/delete-thought.html", context)

@login_required(login_url='login')
def update_profile(request):
    form = UpdateUserForm(instance=request.user)
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        
    context = {'form': form}

    return render(request, "mainapp/update-profile.html", context)

@login_required(login_url='login')
def delete_account(request):
    if request.method == 'POST':
        deleteUser = User.objects.get(username=request.user)
        deleteUser.delete()
        return redirect("")

    return render(request, "mainapp/delete-account.html")