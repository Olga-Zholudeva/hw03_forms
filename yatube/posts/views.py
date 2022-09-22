from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group, User
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.conf import settings


def paginator_func(page_list, request):
    paginator = Paginator(page_list, settings.LIMIT_POSTS)
    page_namber = request.GET.get('page')
    page_obj = paginator.get_page(page_namber)
    return {'page_obj': page_obj}


def index(request):
    context = paginator_func(Post.objects.all(), request)
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    context = {
        'group': group
    }
    context.update(paginator_func(group.posts.all(), request))
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    context = {
        'author': author,
    }
    context.update(paginator_func(author.posts.all(), request))
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'posts/post_detail.html', {'post': post})


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST or None)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect("posts:profile", username=new_post.author)
    else:
        form = PostForm()
    return render(request, "posts/create_post.html", {"form": form})


@login_required
def post_edit(request, post_id):
    edit_post = get_object_or_404(Post, id=post_id)
    if request.user != edit_post.author:
        return redirect("posts:post_detail", post_id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=edit_post)
        if form.is_valid():
            form.save()
            return redirect("posts:post_detail", post_id=post_id)
    else:
        form = PostForm(instance=edit_post)
    context = {"form": form, "is_edit": True}
    return render(request, "posts/create_post.html", context)
