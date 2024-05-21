from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

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