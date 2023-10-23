from django.urls import path
from .views import index, login, register, logout, admin_login

app_name = 'user'
urlpatterns = [
    path('', index),
    path('admin_login/', admin_login),
    path('login/', login),
    path('register/', register),
    path('logout/', logout),
]