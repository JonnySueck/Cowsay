from typing import Text
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Post
from .forms import PostForm
from django.shortcuts import HttpResponseRedirect, render
import subprocess

# Create your views here.
def history(request):
    posts = Post.objects.all()
    number_of_posts = len(posts)
    last = number_of_posts
    if number_of_posts > 10:
        start = number_of_posts - 10
    else:
        start = 0
    posts = Post.objects.all()[start:last]
    return render(request, 'history.html', {'posts': posts})


def pick_cowsay(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            cowsay_type = data['cowsay_type']
            last_post = data['text']
            if cowsay_type == 'Default':
                result = subprocess.run(['cowsay', f'{ last_post }'], capture_output=True)
            if cowsay_type == 'Tux':
                result = subprocess.run(['cowsay', '-f', 'tux', f'{ last_post }'], capture_output=True)
            if cowsay_type == 'Dragon':
                result = subprocess.run(['cowsay', '-f', 'dragon', f'{ last_post }'], capture_output=True)
            if cowsay_type == 'Kitty':
                result = subprocess.run(['cowsay', '-f', 'kitty', f'{ last_post }'], capture_output=True)
            if cowsay_type == 'Skeleton':
                result = subprocess.run(['cowsay', '-f', 'skeleton', f'{ last_post }'], capture_output=True)
            return result


def set_cookies(request):
    initial_welcome = subprocess.run(['cowsay', 'welcome'], capture_output=True)
    welcome = initial_welcome.stdout.decode()
    response = HttpResponse(f'{ welcome }')
    response.set_cookie('program', f'{welcome}')
    return response


def get_cookie(request):
    visit_number = request.COOKIES['program']
    return HttpResponse('the visit number is' + visit_number)


def index_view(request):
    form = PostForm()
    set_cookies(request)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Post.objects.create(
                text = data['text'],
                cowsay_type = data['cowsay_type']
            )
            # get_cookie(request)
            form = PostForm()
            result = pick_cowsay(request)
            results = result.stdout.decode()
            return render(request, 'index.html', {
                'results': results,
                'form': form})
                
    get_cookie(request)
    form = PostForm()
    return render(request, 'index.html', {
        'form': form,
        })