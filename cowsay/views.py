from typing import Text
from django.http import HttpResponse, response
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


def setcookie(request):
    html = HttpResponse("<h1>Dataflair Django Tutorial</h1>")
    if request.COOKIES.get('visits'):
        html.set_cookie('dataflair', 'Welcome Back')
        value = int(request.COOKIES.get('visits'))
        html.set_cookie('visits', value + 1)
    else:
        value = 1
        text = "Welcome for the first time"
        html.set_cookie('visits', value)
        html.set_cookie('dataflair', text)
    return html


def showcookie(request):
    if request.COOKIES.get('visits') is not None:
        value = request.COOKIES.get('visits')
        text = request.COOKIES.get('dataflair')
        html = HttpResponse("<center><h1>{0}<br>You have requested this page {1} times</h1></center>".format(text, value))
        html.set_cookie('visits', int(value) + 1)
        return html
    else:
        return redirect('/setcookie')


def index_view(request):
    form = PostForm()
    showcookie(request)
    show = request.COOKIES['visits']
    try:
        value = request.COOKIES['cookie_name']
    except KeyError:
        # cookie is not set
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                Post.objects.create(
                    text = data['text'],
                    cowsay_type = data['cowsay_type']
                )
                form = PostForm()
                result = pick_cowsay(request)
                setcookie(request)
                results = result.stdout.decode()
                response = HttpResponse('blah')
                return render(request, 'index.html', {
                        'results': results,
                        'form': form,
                        })

        form = PostForm()
        return render(request, 'index.html', {
            'form': form,
            'show': show,
            })
