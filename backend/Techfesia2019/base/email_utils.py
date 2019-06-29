# will contain all email utils
from django.core.mail import send_mail
from django.conf import settings

def welcomeEmail():
    subject = "welcome email"
    from_email = "lambatketan@gmail.com"
    to_email = [ 'ketan.lambat@ymail.com' ]

    content_message = "welcome people this is working"
    send_mail(subject,content_message,from_email,to_email,fail_silently=False) #Changed to false so that we can get the error msg

def welcomeEmailhtml():
    subject = "welcome email (html)"
    from_email = "lambatketan@gmail.com"
    to_email = ['ketan.lambat@ymail.com']

    content_message = "email visible in browser"
    send_mail(subject, content_message, from_email, to_email, fail_silently=False)

