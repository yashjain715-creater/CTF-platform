from django.urls import path, include
from ctf_backend.views import *

urlpatterns = [
    path('',listQuesView, name="listQues"),
    path('submit',submitAnswerView, name="submitAns"),
    path('emailConfirmation',emailConfirmationView,name="emailConfirmation"),
    path('forgotPassword',forgotPasswordView,name="forgotPassword"),  
    path('passwordReset',passwordResetView,name="passwordReset"),
    path('successful',successfulView,name="successful"),  
]