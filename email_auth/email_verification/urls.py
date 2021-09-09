from django.contrib import admin
from django.urls import path
from .views import home, login_attempts, register_attempts, success, token_send_mail, verify, error_page

urlpatterns = [

path('', home , name='home'),
path('login/', login_attempts , name='login'),
path('register/', register_attempts , name='register'),
path('success/', success , name='success'),
path('token_send/', token_send_mail , name='token_send'),
path('verify/<auth_token>', verify , name='verify'),
path('error/', error_page , name='error'),
]
