from typing import Text
from django.http import HttpResponse, response
from django.shortcuts import redirect, render
from .models import Post
from .forms import PostForm
from django.shortcuts import HttpResponseRedirect, render
import subprocess

## todo, set cookie as a tuple or dictionary to reference for cowtype

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
            # print(result)
            return result


# def setcookie(request):
#     last_post = Post.objects.last()
#     text = last_post.text
#     cowsay_type = last_post.cowsay_type
#     html = HttpResponse(
#         "Your post has successfully been submitted <a href='/'>go home</a>")
#     if request.COOKIES.get('lastpost'):
#         value = request.COOKIES.get('lastpost')
#         html.set_cookie('lastpost', last_post)
#         html.set_cookie('cowsay', cowsay_type)
#     else:
#         text = "Welcome for the first time"
#         html.set_cookie('lastpost', text)
#     return html


# def showcookie(request):
#     if request.COOKIES.get('lastpost') is not None:
#         value = request.COOKIES.get('lastpost')
#         print(value)
#         text = request.COOKIES.get('dataflair')
#         html = HttpResponse("<center><h1>{0}<br>You have requested this page {1} times</h1></center>".format(text, value))
#         html.set_cookie('lastpost', value)
#         return html
#     else:
#         return HttpResponseRedirect('/setcookie/')



def index_view(request):
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
                # setcookie('result', result)
                results = result.stdout.decode()
                # response = HttpResponse('blah')
                # response.set_cookie('lastpost', f'{results}')
                return render(request, 'index.html', {'results': results, 'form': form})
    form = PostForm()
    return render(request, 'index.html', {'form': form})
    # showcookie(request)


    # if request.COOKIES.get('lastpost'):
    #     last_post = request.COOKIES.get('lastpost')
    #     cow = request.COOKIES.get('cowsay')
    #     setcookie(request)
    #     # results = last_post.stdout.decode()
    #     response = HttpResponse('blah')
    #     response.set_cookie('lastpost', f'{last_post}')
    # else:
    #     shows = subprocess.run(['cowsay', f'welcome for the first time'], capture_output=True)
    #     results = shows.stdout.decode()

    # form = PostForm()
    # return render(request, 'index.html', {
    #     'form': form,
    #     'show': cow,
    #     })

    

