from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser, Post, Comment
from django.http import HttpResponse
from blog.forms import CommentForm
from .forms import PostForm, RegistrationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
    posts = Post.objects.all().order_by('datePosted')
    return render(request, 'blog/home.html', {'posts': posts})

def post_category(request, category):
    posts = Post.objects.filter(categories__name__contains=category).order_by('datePosted')
    return render(request, "blog/category.html", {'category': category, 'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post)
    form = CommentForm()

    if not post.isPublic:
        if request.method == 'POST' and 'password' in request.POST:
            entered_password = request.POST.get('password')
            if entered_password == post.password:
                request.session['unlocked_post'] = pk
            else:
                error_message = "Incorrect password"
                return render(request, 'blog/password_prompt.html', {'post': post, 'error_message': error_message})

        if request.session.get('unlocked_post') != pk:
            return render(request, 'blog/password_prompt.html', {'post': post})

    if request.method == 'POST' and 'content' in request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=request.user,
                content=form.cleaned_data["content"],
                post=post,
            )
            comment.save()
            return HttpResponseRedirect(request.path_info)

    context = {
        "post": post,
        "comments": comments,
        "form": form,
    }
    return render(request, "blog/detail.html", context)

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            print('got POST and form is valid')
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m() 
            return redirect('post_detail', pk=post.pk)
        print('got POST but form is invalid')
        print(form.errors)
    else:
        form = PostForm()
    return render(request, 'blog/add_post.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            return redirect('blog-home')
    else:
        form = RegistrationForm()
    return render(request, 'blog/register.html', {'form': form})
    
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(username)
        print(password)
        print(request)
        print(user)

        if user is not None:
            login(request, user)
            print("logged in")
            return redirect('blog-home') 
    context = {}
    return render(request, 'blog/login.html', context)