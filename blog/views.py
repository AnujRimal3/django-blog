from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import PostForm
from .models import Downvote, Post, Upvote


def post_list(request):
    posts = Post.objects.all().order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password1'),
            )
            login(request, user)
            return redirect('post_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def author_detail(request, pk):
    """Send an author link to that author's profile page."""
    author = get_object_or_404(User, pk=pk)
    return redirect('profile', username=author.username)


@login_required
def upvote_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    # One vote per user per post: voting one way removes the opposite vote.
    Downvote.objects.filter(post=post, user=request.user).delete()
    Upvote.objects.get_or_create(post=post, user=request.user)
    return redirect('post_list')


@login_required
def downvote_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    Upvote.objects.filter(post=post, user=request.user).delete()
    Downvote.objects.get_or_create(post=post, user=request.user)
    return redirect('post_list')


@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form, 'heading': 'New post'})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:  # only the author may edit
        return redirect('post_detail', pk=post.pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form, 'heading': 'Edit post'})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:  # only the author may delete
        return redirect('post_detail', pk=post.pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})


@login_required
def my_profile(request):
    return redirect('profile', username=request.user.username)


def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile_user).order_by('-published_date')
    return render(request, 'blog/profile.html',
                  {'profile_user': profile_user, 'posts': posts})
