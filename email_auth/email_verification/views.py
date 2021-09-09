from django.shortcuts import render, redirect

from django.contrib import messages

'''import reverse_lazy and it will redirect our user to a certain parts of our page or application'''
from django.urls import reverse_lazy

'''import the models from the models.py'''
from . models import Profile
from django.contrib.auth.models import User

'''import uuid so that we can generate unique strings for our token'''
import uuid

'''import your django settings so that mail can be sent to the user during her/his registration process'''
from django.conf import settings
from django.core.mail import send_mail

def home(request):
    return render(request, 'home.html')

def login_attempts(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        '''get the username and password of the user and match it from the database
        if the user is not present than redirect the user to the registration page'''
        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request,'User not found. Please Register and try again!')
            return redirect('login')

        profile_obj = Profile.objects.create(user = user_obj).first()

        '''if email is not verified of the user then redirect user to the registration page'''
        if not profile_obj.email_verified:
            messages.success(request,'your profile is not verified. check your mail!')
            return redirect('login')

    return render(request, 'login.html')

def register_attempts(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            #checking if the username or email address has already been registered
            if User.objects.filter(username=username).first():
                '''send the user to the tasks list page'''
                messages.success(request,'Username is taken')
                return redirect('register')
            if User.objects.filter(email=email).first():
                messages.success(request,'this email address has already been registered')
                return redirect('register')

            user_obj = User.objects.create(username = username, email = email)
            user_obj.set_password(password)
            user_obj.save()
            token = str(uuid.uuid4())
            #str(uuid.uuid4()) will return a string in this format bb4e9c89-4266-401b-907d-e20a4417581f
            #and every time our uuid.uuid4() will return a unique string
            profile_obj = Profile.objects.create(user = user_obj, auth_token = token)
            profile_obj.save()

            '''send mail to the user that has recently registered onto your site and then redirect the user to the next page'''
            sen_mail_after_registration(email, token)
            '''redirect user to the token_send_mail page'''
            return redirect('token_send')
        except Exception as e:
            print(e)

    return render(request, 'register.html')

def success(request):
    return render(request, 'success.html')

def token_send_mail(request):
    return render(request, 'token_send.html')

def error_page(request):
    return render(request, 'error.html')

def verify(request, auth_token):
    '''query the profile object from the database'''
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
        '''if the profile_obj is not null then make email_verified BooleanField = TRUE'''
        if profile_obj:
            if profile_obj.email_verified:
                messages.success(request,'Your account is already verified')
                '''if the user profile is already verified then send the user to the login page'''
                return redirect('login')

            profile_obj.email_verified = True
            profile_obj.save()
            messages.success(request,'Your account has been verified')
            '''as soon as profile_obj.email_verified becomes True we have to redirect the user to the home page'''
            return redirect('login')
        else:
            '''if the profile_obj is null then send the user to the error page'''
            return redirect('error')
    except Exception as e:
        print(e)

'''this function is reposible for sending the token to our user during his/her reigtration process'''
def sen_mail_after_registration(email, token):
    subject = 'Your account needs to be verified'
    message = f'Hi This is Aditya thank you for choosing my website To do Task management web application paste the link to verify your account http://127.0.0.1:8000/verify/{token}'

    #now here create your settings for email verification
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject,message,email_from,recipient_list)
