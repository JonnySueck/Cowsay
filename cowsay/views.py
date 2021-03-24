from django.http import HttpResponse
from django.shortcuts import render
from .models import Post
from .forms import PostForm
import subprocess


# Create your views here.
def history(request):
    posts = Post.objects.all()
    number_of_posts = len(posts)
    last = number_of_posts
    first = 1
    if number_of_posts > 10:
        first = number_of_posts - 10
    post = Post.objects.get(id=first)
    cowsay_type = post.cowsay_type
    message = post.text
    cow = subprocess.run(['cowsay', '-f', f'{cowsay_type}',
                          f'{message}'], capture_output=True)
    results = cow.stdout.decode()
    if number_of_posts > 10:
        start = number_of_posts - 10
    else:
        start = 0
    posts = Post.objects.all()[start:last]
    return render(request, 'history.html', {
        'posts': posts,
        'results': results
        })


def index_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Post.objects.create(
                text=data['text'],
                cowsay_type=data['cowsay_type']
            )
            text = data['text']
            cowsay_type = data['cowsay_type']
            form = PostForm()
            html = HttpResponse(
                "Your post has successfully been submitted \
                 <a href='/'>go home</a>")
            html.set_cookie('lastpost', text)
            html.set_cookie('cowsay', cowsay_type)
            return html

    if request.COOKIES.get('lastpost'):
        form = PostForm()
        last_post = request.COOKIES.get('lastpost')
        cowsay_type = request.COOKIES.get('cowsay')
        cow = subprocess.run(['cowsay', '-f', f'{cowsay_type}',
                             f'{last_post}'], capture_output=True)
        results = cow.stdout.decode()
        message = 'welcome back to cowsay'
        return render(request, 'index.html', {
            'show': results, 'form': form,
            'welcome': message})

    shows = subprocess.run(['cowsay', 'Welcome!'],
                           capture_output=True)
    result = shows.stdout.decode()
    form = PostForm()
    return render(request, 'index.html', {
        'form': form,
        'show': result,
        })
