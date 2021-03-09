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


def index_view(request):
    if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                Post.objects.create(
                    text = data['text'],
                    cowsay_type = data['cowsay_type']
                )
                text = data['text']
                cowsay_type = data['cowsay_type']
                form = PostForm()
                result = pick_cowsay(request)
                results = result.stdout.decode()
                html = HttpResponse("Your post has successfully been submitted <a href='/'>go home</a>")
                html.set_cookie('lastpost', text)
                html.set_cookie('cowsay', cowsay_type)
                return html

    if request.COOKIES.get('lastpost'):
        form = PostForm()
        last_post = request.COOKIES.get('lastpost')
        cowsay_type = request.COOKIES.get('cowsay')
        result = pick_cowsay(request)
        cow = subprocess.run(['cowsay', '-f', f'{cowsay_type}', f'{last_post}'], capture_output=True)
        results = cow.stdout.decode()
        return render(request, 'index.html', {'show': results, 'form': form})

    shows = subprocess.run(['cowsay', f'welcome for the first time'], capture_output=True)
    result = shows.stdout.decode()
    form = PostForm()
    return render(request, 'index.html', {
        'form': form,
        'show': result,
        })

    

