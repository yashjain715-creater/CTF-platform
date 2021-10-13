from django.shortcuts import render
# Create your views here.


def listQuesView(request):
    return render(request,'listQues.html')

def emailConfirmationView(request):
    return render(request,'emailConfirmation.html')

def forgotPasswordView(request):
    return render(request,'forgotPassword.html')

def passwordResetView(request):
    return render(request,'passwordReset.html')

def successfulView(request):
    return render(request,'successful.html')

def submitAnswerView(request):
    pass

