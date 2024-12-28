from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

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
    path('profile/delete', views.delete_account, name='delete-account'),

    # Password management
    path('password/reset', auth_views.PasswordResetView.as_view(template_name='mainapp/passwd-reset.html'), name='password_reset'),
    path('password/reset/sent', auth_views.PasswordResetDoneView.as_view(template_name='mainapp/passwd-reset-sent.html'), name='password_reset_done'),
    path('password/reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='mainapp/passwd-reset-form.html'), name='password_reset_confirm'),
    path('password/reset/complete', auth_views.PasswordResetCompleteView.as_view(template_name='mainapp/passwd-reset-complete.html'), name='password_reset_complete'),
]
