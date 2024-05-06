from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Post
from accounts.models import Profile
from django.contrib.auth.models import User

# Create your views here.

def mainpage(request):
    context = {
        'element': ['Model', 'Template', 'View'],
    }
    return render(request, 'main/mainpage.html', context)

def secondpage(request):
    posts = Post.objects.all()
    return render(request, 'main/secondpage.html', {'posts':posts})

def new_post(request):
    return render(request, 'main/new-post.html')

def detail(request, id):
    post = get_object_or_404(Post, pk=id)
    return render(request, 'main/detail.html', {'post':post})

def create(request):
    new_post = Post()

    new_post.title = request.POST['title']
    new_post.writer = request.user
    new_post.post_type = request.POST['post_type']
    new_post.image = request.FILES.get('image')
    new_post.body = request.POST['body']
    new_post.pub_date = timezone.now()

    new_post.save()

    return redirect('main:detail', new_post.id)

def edit(request, id):
    edit_post = Post.objects.get(pk=id)
    return render(request, 'main/edit.html', {'post':edit_post})

def update(request, id):
    update_post = Post.objects.get(pk=id)

    update_post.title = request.POST['title']
    update_post.writer = request.user
    update_post.post_type = request.POST['post_type']
    update_post.image = request.FILES.get('image')
    update_post.body = request.POST['body']
    update_post.pub_date = timezone.now()

    update_post.save()

    return redirect('main:detail', update_post.id)

def delete(request, id):
    delete_post = Post.objects.get(pk=id)
    delete_post.delete()

    return redirect('main:secondpage')

