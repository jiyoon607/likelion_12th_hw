from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
import re
from .models import Post, Comment, Tag
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
    if request.method == 'GET':
        comments = Comment.objects.filter(post=post)
        return render(request, 'main/detail.html', {'post':post, 'comments':comments})

    elif request.method == 'POST':
        new_comment = Comment()

        new_comment.post = post
        new_comment.writer = request.user
        new_comment.content = request.POST['content']
        new_comment.pub_date = timezone.now()

        new_comment.save()

        #댓글 해시태그 만들기
        words = re.split(r'[\s]', new_comment.content)
        tag_list = []

        for w in words:
            if len(w)>1:
                if w[0] == '#':
                        tag_list.append(w[1:])

        for t in tag_list:
            tag, boolean = Tag.objects.get_or_create(name=t)
            new_comment.tag.add(tag.id)

        return redirect('main:detail', post.id)

def create(request):
    if request.user.is_authenticated:
        new_post = Post()

        new_post.title = request.POST['title']
        new_post.writer = request.user
        new_post.post_type = request.POST['post_type']
        new_post.image = request.FILES.get('image')
        new_post.body = request.POST['body']
        new_post.pub_date = timezone.now()

        new_post.save()

        words = re.split(r'[\s]', new_post.body) #기존 split함수가 공백 오류나서 수정함
        tag_list = []

        for w in words:
            if len(w)>1:
                if w[0] == '#':
                        tag_list.append(w[1:])

        for t in tag_list:
            tag, boolean = Tag.objects.get_or_create(name=t)
            new_post.tag.add(tag.id)

        return redirect('main:detail', new_post.id)
    
    else:
        return redirect('accounts:login')

def edit(request, id):
    edit_post = Post.objects.get(pk=id)
    return render(request, 'main/edit.html', {'post':edit_post})

def update(request, id):
    update_post = Post.objects.get(pk=id)
    if request.user.is_authenticated and request.user == update_post.writer:
        update_post.title = request.POST['title']
        update_post.post_type = request.POST['post_type']
        update_post.body = request.POST['body']
        update_post.pub_date = timezone.now()

        if request.FILES.get('image'):
            update_post.image = request.FILES['image']

        update_post.tag.clear()

        words = re.split(r'[\s]', update_post.body) #기존 split함수가 공백 오류나서 수정함
        tag_list = []

        for w in words:
            if len(w)>1:
                if w[0] == '#':
                        tag_list.append(w[1:])

        for t in tag_list:
            tag, boolean = Tag.objects.get_or_create(name=t)
            update_post.tag.add(tag.id)


        update_post.save()

        return redirect('main:detail', update_post.id)
    return redirect('accounts:login', update_post.id)

def delete(request, id):
    delete_post = Post.objects.get(pk=id)
    delete_post.delete()

    return redirect('main:secondpage')

def deleteComment(request, id):
    delete_comment = Comment.objects.get(pk=id)
    post = Post.objects.get(pk=delete_comment.post.id) #댓글이 달린 post의 id를 가져오기 위함, redirect하기 위함
    delete_comment.delete()

    return redirect('main:detail', post.id) 


def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'main/tag-list.html', {'tags':tags})

def tag_posts(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    comments = tag.comment.all()
    posts = []
    for c in comments:
        posts += Post.objects.filter(id=c.post_id)
    posts += tag.post.all()
    temp_posts = set(posts) #중복제거
    posts = list(temp_posts)
    return render(request, 'main/tag-post.html', {'tag':tag, 'posts':posts})

def likes(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.like.all():
        post.like.remove(request.user)
        post.like_count -= 1
        post.save()
    else:
        post.like.add(request.user)
        post.like_count += 1
        post.save()
    return redirect('main:detail', post.id)