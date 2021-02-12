from django.shortcuts import redirect, render
from .models import Post
from .forms import PostForm
from django.shortcuts import HttpResponseRedirect, render

# Create your views here.
def history(request):
    posts = Post.objects.all()
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
            form = PostForm()
            return render(request, 'index.html', {'form': form})

    form = PostForm()
    return render(request, 'index.html', {'form': form})