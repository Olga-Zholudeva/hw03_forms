from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group, User
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from posts.utils import paginator_func


def index(request):
    index_list = Post.objects.all()
    context = {
        'page_obj': paginator_func(index_list, request)
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    group_list = group.posts.all()
    context = {
        'group': group,
        'page_obj': paginator_func(group_list, request)
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    profile_list = author.posts.all()
    context = {
        'author': author,
        'page_obj': paginator_func(profile_list, request)
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'posts/post_detail.html', {'post': post})


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect("posts:profile", username=new_post.author)
    return render(request, "posts/create_post.html", {"form": form})


@login_required
def post_edit(request, post_id):
    edit_post = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None, instance=edit_post)
    if request.user != edit_post.author:
        return redirect("posts:post_detail", post_id=post_id)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect("posts:post_detail", post_id=post_id)
    context = {"form": form, "is_edit": True}
    return render(request, "posts/create_post.html", context)
