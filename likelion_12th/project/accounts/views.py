from django.shortcuts import render, redirect
from django.contrib import auth
from .models import Profile
from django.contrib.auth.models import User

# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('main:mainpage')
        else:
            return render(request, 'accounts/login.html')

    elif request.method == 'GET':
        return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    return redirect('main:mainpage')

def signup(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['confirm']:
            user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password']
            )

            user.profile.name = request.POST['username']
            user.profile.gender = request.POST['gender']
            user.profile.birth = request.POST['birth']
            user.profile.email = request.POST['email']

            user.profile.save()

            auth.login(request, user)
            return redirect('/')

    elif request.method == 'GET':
        return render(request, 'accounts/signup.html')
