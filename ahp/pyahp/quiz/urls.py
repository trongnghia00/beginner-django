from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_view, name=''),
    path('quiz', views.quiz_view, name='quiz'),
]