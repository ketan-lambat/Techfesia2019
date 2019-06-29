# will contain all email utils
from django.core import mail
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def welcomeEmail():
    subject = "welcome email"
    from_email = "lambatketan@gmail.com"
    to_email = [ 'ketan.lambat@ymail.com' ]

    content_message = "welcome people this is working"
    send_mail(subject,content_message,from_email,to_email,fail_silently=False) #Changed to false so that we can get the error msg

def welcomeEmailhtml():
    subject = "welcome email (html)"
    html_message = render_to_string('emails/welcome.html', {'context': 'values'})
    plain_message = strip_tags(html_message)
    from_email = "lambatketan@gmail.com"
    to_email = ['ketan.lambat@ymail.com']

    content_message = "email visible in browser"
    mail.send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
   # send_mail(subject, content_message, from_email, to_email, fail_silently=False)

    # https://stackoverflow.com/questions/3005080/how-to-send-html-email-with-django-with-dynamic-content-in-it