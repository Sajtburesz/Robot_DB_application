# myproject/myproject/urls.py
from django.urls import path
from thesis_backend.login_views import register, login

urlpatterns = [
    path('api/register', register, name='register'),
    path('api/login', login, name='login'),
]