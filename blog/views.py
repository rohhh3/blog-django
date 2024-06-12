from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, CustomUser
from blog.forms import CommentForm
from .forms import PostForm, RegistrationForm, LoginForm, UpdateUserForm, UpdateUserPasswordForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.core.files.storage import default_storage

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

@login_required
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
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully")
                return redirect('blog-home')
            else:
                messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, 'blog/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, ("Logged out succesfully"))
    return redirect('blog-home')

@login_required
def update_user(request):
    current_user = CustomUser.objects.get(id=request.user.id)
    user_form = UpdateUserForm(request.POST or None, request.FILES or None, instance=current_user)
    password_form = UpdateUserPasswordForm(user=request.user, data=request.POST or None)

    if request.method == 'POST':
        if user_form.is_valid() and password_form.is_valid():
            user = user_form.save(commit=False)
            if 'avatar' in request.FILES:
                user.avatar = request.FILES['avatar']
            user.save()
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "User profile and password have been updated")
            return redirect('blog-home')
        elif user_form.is_valid():
            user = user_form.save(commit=False)
            if 'avatar' in request.FILES:
                user.avatar = request.FILES['avatar']
            user.save()
            messages.success(request, "User profile has been updated")
            return redirect('blog-home')

        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('update_user')

    return render(request, 'blog/update_user.html', {'user_form': user_form, 'password_form': password_form})

def user_profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    posts = Post.objects.filter(author=user).order_by('-datePosted')
    return render(request, 'blog/profile.html', {'profile_user': user, 'posts': posts})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        messages.error(request, "You are not authorized to edit this post.")
        return redirect('post_detail', pk=pk)
    
    old_thumbnail = post.thumbnail.path if post.thumbnail else None

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            if not request.FILES.get('thumbnail') and 'thumbnail-clear' in request.POST and old_thumbnail:
                default_storage.delete(old_thumbnail)
            elif request.FILES.get('thumbnail') and old_thumbnail:
                default_storage.delete(old_thumbnail)
                
            form.save()
            messages.success(request, "Post has been updated.")
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/edit_post.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        messages.error(request, "You are not authorized to delete this post.")
        return redirect('post_detail', pk=pk)
    
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post has been deleted.")
        return redirect('blog-home')
    return render(request, 'blog/delete_post.html', {'post': post})

@login_required
def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.author:
        messages.error(request, "You are not authorized to edit this comment.")
        return redirect('post_detail', pk=comment.post.pk)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Comment has been updated.")
            return redirect('post_detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/edit_comment.html', {'form': form})

@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.author:
        messages.error(request, "You are not authorized to delete this comment.")
        return redirect('post_detail', pk=comment.post.pk)

    if request.method == "POST":
        post_pk = comment.post.pk
        comment.delete()
        messages.success(request, "Comment has been deleted.")
        return redirect('post_detail', pk=post_pk)
    return render(request, 'blog/delete_comment.html', {'comment': comment})
