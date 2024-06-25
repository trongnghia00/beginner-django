from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from .models import Task

from .forms import TaskForm

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
    return render(request, "appone/register.html")

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

def task_form(request):
    # pass
    form = TaskForm()
    context = {'TaskForm': form}
    return render(request, "appone/task_form.html", context)