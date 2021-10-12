from django.shortcuts import render, redirect
from django.contrib.auth import login,logout,authenticate
from .models import UserAccount

def loginView(request):
    context={
        "visibility":"none",
    }
    if request.method=="POST":
        username= request.POST.get('username')
        password= request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return render(request, 'login.html',context)
    return render(request, 'login.html',context)

def logoutView(request):
    logout(request)
    context={
        'visibility':"",
    }
    return render(request, 'login.html',context)

def registerView(request):
    context={
        'visibility':"none",
    }
    if request.method=="POST":
        username= request.POST.get('username')
        email = request.POST.get('email')
        password= request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            context['visibility']=""
            return render(request, 'register.html',context)
        user = UserAccount.objects.create_user(username=username,email=email,password=password)
        user.first_name=request.POST.get('first_name')
        user.last_name=request.POST.get('last_name')
        user.year=request.POST.get('year')
        user.gender=request.POST.get('gender')
        user.college_name=request.POST.get('college_name')
        user.mobile_no=request.POST.get('mobile_no')
        user.branch=request.POST.get('branch')
        if user is not None:
            user.save()
            login(request, user)
            return redirect("/")
        else:
            return render(request, 'register.html',context)
    return render(request, 'register.html',context)