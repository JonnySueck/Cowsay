from typing import Text
from django.shortcuts import redirect, render
from .models import Post
from .forms import PostForm
from django.shortcuts import HttpResponseRedirect, render
import subprocess, cowsay

# Create your views here.
def history(request):
    posts = Post.objects.all()[:10]
    return render(request, 'history.html', {'posts': posts})

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
            form = PostForm()
            return render(request, 'index.html', {
                'last_post': last_post,
                'form': form})

    form = PostForm()
    return render(request, 'index.html', {'form': form})