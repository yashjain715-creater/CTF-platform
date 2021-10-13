from django.contrib import admin
from django.urls import path, include
from authentication.views import *

urlpatterns = [
    path('login',loginView, name="login"),
    path('logout',logoutView, name="logout"),
    path('register',registerView, name="register"),
    path('resetQuery',resetQueryView, name="resetQuery"),
    path('activate/<uidb64>/<token>/', ActivateAccountView,name="activate-account"),   
    path('password_reset/<uidb64>/<token>/', ResetPasswordView,name="password-reset-confirm"),   
]