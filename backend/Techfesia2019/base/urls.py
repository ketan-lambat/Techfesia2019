from django.urls import path, include
from . import views

urlpatterns = [
    #path('', views.email_welcome),
    path('', views.email_test, name="test_email"),
    path('welcome/', views.email_welcome, name="welcome_email"),
]