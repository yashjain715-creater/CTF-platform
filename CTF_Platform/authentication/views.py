from django.shortcuts import render, redirect
from django.contrib.auth import login,logout,authenticate
from .models import UserAccount
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str, smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util

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
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse('activate-account', kwargs={'uidb64': uidb64, 'token': token})
            absurl = 'http://' + current_site + relativeLink
            email_body = 'Hello '+user.username+',\nUse this link to activate your account: \n'+absurl
            data = {'email_body': email_body, 'to_mail': user.email, 'email_subject': 'Activate Your Udyam Password'}
            Util.send_email(data)
            # render verifyYourAccount page
            return render(request, 'verifyYourAccount.html')
        else:
            return render(request, 'register.html',context)
    return render(request, 'register.html',context)


def ActivateAccountView(request,uidb64, token):
    try:
        id = smart_str(urlsafe_base64_decode(uidb64))
        user = UserAccount.objects.get(id=id)

        if not PasswordResetTokenGenerator().check_token(user, token):
            # invalid token
            return render(request, 'register.html')      
        user.is_active=True
        user.save()
        login(request, user)
        # redirect to home page
        return redirect("/") 

    except DjangoUnicodeDecodeError as identifier:
        # invalid token
        return render(request, 'register.html')   