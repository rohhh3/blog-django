from django.shortcuts import render, redirect
from .models import CustomUser, Post, Comment
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
# Create your views here.
def home(request):
    posts = Post.objects.all().order_by('datePosted')
    return render(request, 'blog/home.html', {'posts': posts})

def post_category(request, category):
    posts = Post.objects.filter(categories__name__contains=category).order_by('datePosted')
    return render(request, "blog/category.html", {'category': category, 'posts': posts})

def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(post=post)
    return render(request, "blog/detail.html", {'post': post, 'comments': comments})

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