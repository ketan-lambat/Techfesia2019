# will contain all email utils
from django.core.mail import send_mail
from django.conf import settings

def welcomeEmail():
    subject = "welcome email"
    from_email = "hrishabh2203@gmail.com"
    to_email = [ 'hrishabh.p18@iiit.in' ]

    content_message = "welcome people this is working"
    send_mail(subject,content_message,from_email,to_email,fail_silently=True)