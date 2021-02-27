from typing import Text
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
    start = number_of_posts - 10
    posts = Post.objects.all()[start:last]
    return render(request, 'history.html', {'posts': posts})


def pick_cowsay(request):
    ...

def index_view(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Post.objects.create(
                text = data['text']
            )
            last_post = data['text']
            cowsay_type = data['cowsay_type']
            form = PostForm()
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
            results = result.stdout.decode()
            return render(request, 'index.html', {
                'results': results,
                'form': form})

    form = PostForm()
    return render(request, 'index.html', {'form': form})