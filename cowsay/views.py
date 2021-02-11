from django.shortcuts import render
from .models import Post
from .forms import PostForm

# Create your views here.
def index(request):
    form = Post.objects.all()
    return render(request, 'index.html', {'form': form})
