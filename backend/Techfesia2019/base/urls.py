from django.urls import path, include
from . import views

urlpatterns = [
    #path('', views.email_welcome),
    path('', views.email_test),
    path('welcome/', views.email_welcome),
]