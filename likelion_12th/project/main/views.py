from django.shortcuts import render

# Create your views here.

def mainpage(request):
    context = {
        'element': ['Model', 'Template', 'View'],
    }
    return render(request, 'main/mainpage.html', context)

def secondpage(request):
    context = {
        'number': 6,
        'members': ['민경', '유진', '서현', '세라', '태준', '수용', '지윤'],
    }
    return render(request, 'main/secondpage.html', context)