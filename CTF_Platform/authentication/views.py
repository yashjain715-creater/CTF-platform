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
        user.first_name=request.POST.get('name')
        user.year=request.POST.get('year')
        user.college_name=request.POST.get('college_name')
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
        return render(request,'account_activated.html')

    except DjangoUnicodeDecodeError as identifier:
        # invalid token
        return render(request, 'register.html')   

def resetQueryView(request):
    if request.method=="POST":
        email = request.POST.get('email')
        if UserAccount.objects.filter(email=email).exists():
            user = UserAccount.objects.get(email=email)
            if user.is_active==False:
                print("account not active")
                return render(request, 'passwordReset.html')
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            absurl = 'http://' + current_site + relativeLink
            email_body = 'Hello '+user.username+',\nUse this link to reset your password: \n'+absurl
            data = {'email_body': email_body, 'to_mail': user.email, 'email_subject': 'Reset Your Udyam Password'}
            Util.send_email(data)
            return render(request, 'verifyYourAccount.html')
        else:
            return render(request, 'getEmail.html')

    return render(request, 'getEmail.html')

def ResetPasswordView(request,uidb64, token):
    if request.method=="POST":
        id = smart_str(urlsafe_base64_decode(uidb64))
        user = UserAccount.objects.get(id=id)
        print("request",user,token)
        if not PasswordResetTokenGenerator().check_token(user, token):
            print("error")
            return render(request, 'passwordReset.html')
        user.password=request.POST.get('password')
        user.save()
        return render(request, 'reset_successful.html')
    return render(request, 'passwordReset.html')   