from django.shortcuts import render
from .models import Post, PostNew
from .forms import PostForm
from django.shortcuts import HttpResponseRedirect, render

# Create your views here.
def index(request):
    form = PostNew.objects.all()
    return render(request, 'index.html', {'form': form})

def history(request):
    posts = PostNew.objects.all()
    return render(request, 'history.html', {'posts': posts})

def post_new(request):
    if request.method == 'POST':
        # create an instance and fill with request data
        form = PostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Post.objects.create(
                text = data.get('text'),
            )
            return HttpResponseRedirect('/')
   
    form = PostForm()
    return render(request, 'index.html', {'form': form})