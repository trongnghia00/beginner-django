from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage),
    path("task/", views.task),
    path("task/<int:id>/", views.task_detail),
    path("register/", views.register),
]