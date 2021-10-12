from django.contrib import admin
from django.urls import path, include
from authentication.views import *

urlpatterns = [
    path('',loginView, name="login"),
    path('logout',logoutView, name="logout"),
    path('register',registerView, name="register"),   
]