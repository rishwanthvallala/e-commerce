from django.shortcuts import render

# Create your views here.
from django.shortcuts import render


def login(request):
    return render(request, 'users/auth/login.html')

def signup(request):
    return render(request, 'users/auth/signup.html')

def forgot_password(request):
    return render(request, 'users/auth/forgot-password.html')
