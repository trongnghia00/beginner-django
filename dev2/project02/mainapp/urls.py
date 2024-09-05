from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name=''),
    path('register', views.register, name='register'),
    path('login', views.my_login, name='login'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('logout', views.user_logout, name='logout'),

    path('thought/', views.my_thoughts, name='my-thoughts'),
    path('thought/create', views.create_thought, name='create-thought'),
    path('thought/update/<str:id>', views.update_thought, name='update-thought'),
    path('thought/delete/<str:id>', views.delete_thought, name='delete-thought'),
    
    path('profile/update', views.update_profile, name='update-profile'),
]
