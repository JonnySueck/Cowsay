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
                html = HttpResponse("Your post has successfully been submitted <a href='/'>go home</a>")
                html.set_cookie('lastpost', text)
                html.set_cookie('cowsay', cowsay_type)
                return html

    if request.COOKIES.get('lastpost'):
        form = PostForm()
        last_post = request.COOKIES.get('lastpost')
        cowsay_type = request.COOKIES.get('cowsay')
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

    

