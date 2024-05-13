from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import CustomUser, Post, Comment
from django.http import HttpResponse
from blog.forms import CommentForm
from .forms import PostForm
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
    post = Post.objects.get(pk=pk)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=request.user,
                content=form.cleaned_data["content"],
                post=post,
            )
            comment.save()
            return HttpResponseRedirect(request.path_info)

    comments = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "comments": comments,
        "form": CommentForm(),
    }
    return render(request, "blog/detail.html", context)

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/add_post.html', {'form': form})

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        hashed_password = make_password(password)  # Hash the password

        # Create and save the user
        user = CustomUser.objects.create(username=username, email=email, password=hashed_password)
        user.save()
        
        # Redirect to a success page or any other page
        return redirect('blog-home')
    else:
        return render(request, 'blog/register.html')
    
# def login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             email = request.POST.get('email')
#             password = request.POST.get('password')
#             user = authenticate(email=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('blog-home')  
#         else: 
#             return render(request, 'blog/login.html', {'form': form})
#     else:
#         form = AuthenticationForm()
#         return render(request, 'blog/login.html', {'form': form})

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