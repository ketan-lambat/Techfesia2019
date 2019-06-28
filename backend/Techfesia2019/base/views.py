from django.shortcuts import render
from django.http import HttpResponse
from . import email_utils

def email_test(request):
    print("-------------sending mail---------------")
    email_utils.welcomeEmail()
    print("----------------done--------------------")
    return HttpResponse(status=202)
    