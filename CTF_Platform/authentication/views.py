from django.shortcuts import render
from django.contrib.auth import login,logout,authenticate
# Create your views here.


def loginView(request):
    return render(request,'login.html')

def logoutView(request):
    pass

def registerView(request):
    return render(request,'register.html')
