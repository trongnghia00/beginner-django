from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name=""),
    path("task/", views.task, name="task"),
    path("task/<int:id>/", views.task_detail, name="task_detail"),
    path("create_task/", views.create_task, name="create_task"),
    path("register/", views.register, name="register"),
]