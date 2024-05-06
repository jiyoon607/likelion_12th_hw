from django.shortcuts import render, redirect

from main.models import Post
from accounts.models import Profile
from django.contrib.auth.models import User
# Create your views here.

def mypage(request):
    myposts = Post.objects.filter(writer=request.user)
    return render(request, 'users/mypage.html', {'myposts':myposts})
