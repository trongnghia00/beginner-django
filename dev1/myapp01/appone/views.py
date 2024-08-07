from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse, Http404

from .models import Task

from .forms import TaskForm, CreateUserForm, LoginForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def homepage(request):
    studentList = [
        {
            'id': 1,
            'name': 'Nghia',
            'city': 'HCM'
        },
        {
            'id': 2,
            'name': 'Trong',
            'city': 'BD'
        },
        {
            'id': 3,
            'name': 'Dinh',
            'city': 'Hue'
        }
    ]
    data = {'myList': studentList}
    return render(request, "appone/index.html", data)

def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('User created')
    
    context = {'RegisterForm': form}

    return render(request, "appone/register.html", context)

def mylogin(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("dashboard")
            
    context = {'LoginForm': form}

    return render(request, "appone/login.html", context)

@login_required
def dashboard(request):
    return render(request, "appone/dashboard.html")

def userLogout(request):
    logout(request)
    return redirect("")

def task(request):
    queryDataAll = Task.objects.all()
    context = {'allTasks' : queryDataAll}
    return render(request, "appone/task.html", context)

def task_detail(request, id) :
    if Task.objects.filter(id=id).exists():
        querySingleData = Task.objects.get(id=id)
    else: 
        querySingleData = {'id': 0}
    context = {'singleTask' : querySingleData}
    return render(request, "appone/task_detail.html", context)

def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task')
    else:
        form = TaskForm()
    context = {'TaskForm': form}
    return render(request, "appone/create_task.html", context)

def update_task(request, id):
    if Task.objects.filter(id=id).exists():
        task = Task.objects.get(id=id)
    else: 
        raise Http404("Task not found")
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid() :
            form.save()
            return redirect('task')
    else:
        form = TaskForm(instance=task)
    
    context = {'TaskForm': form}
    return render(request, "appone/update_task.html", context)

def delete_task(request, id):
    if Task.objects.filter(id=id).exists():
        task = Task.objects.get(id=id)
    else: 
        raise Http404("Task not found")
    
    if request.method == 'POST':
        task.delete()
        return redirect('task')
    
    context = {'task': task}
    return render(request, "appone/delete_task.html", context)