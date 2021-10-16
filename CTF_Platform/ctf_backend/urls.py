from django.urls import path, include
from ctf_backend.views import *

urlpatterns = [
    path('',listQuesView, name="listQues"),
]