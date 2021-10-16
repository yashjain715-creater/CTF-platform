from django.shortcuts import render
# Create your views here.


def listQuesView(request):
    return render(request,'listQues.html')

