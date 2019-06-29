from django.shortcuts import render
from django.http import HttpResponse
from . import email_utils

def email_test(request):
    print("-------------sending mail---------------")
    email_utils.welcomeEmail()
    print("----------------done--------------------")
    return HttpResponse(status=202)

def email_welcome(request):
    print("********Sending Welcome Mail*********")
    email_utils.welcomeEmailhtml()
    print("*****Mail Sent*****")
    #return HttpResponse(status=202)
    return render(request, 'emails/welcome.html')
