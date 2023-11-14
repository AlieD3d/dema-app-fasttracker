from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from posts.forms import CommentForm, PostForm
from posts.models import Post, Group, User, Follow
from posts.utils import pagination


def index(request):
    posts = Post.objects.select_related('group', 'author').all()
    page_obj = pagination(request, posts)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_post(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.select_related('group', 'author').all()
    page_obj = pagination(request, post_list)
    context = {
        "page_obj": page_obj,
        "group": group
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    post_list = profile_user.posts.select_related('group', 'author').all()
    page_obj = pagination(request, post_list)
    if request.user.is_authenticated:
        following = Follow.objects.filter(
            user=request.user, author=profile_user
        ).exists()
    else:
        following = False
    context = {
        'page_obj': page_obj,
        'profile_user': profile_user,
        'following': following
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post.objects.select_related('group', 'author'),
                             pk=post_id)
    user = get_object_or_404(User,
                             username=post.author)
    post_number = user.posts.filter(author=user).count()
    comments = post.comments.all()
    form = CommentForm()
    context = {
        'post': post,
        'post_number': post_number,
        'comments': comments,
        'form': form,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    user_obj = request.user
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', username=post.author)
    context = {
        'form': form,
        'user_obj': user_obj,
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post.objects.select_related().all(), pk=post_id)
    if post.author != request.user:
        return redirect('posts:index')
    form = PostForm(request.POST or None,
                    instance=post,
                    files=request.FILES or None)
    if not form.is_valid():
        context = {
            'form': form,
            'is_edit': True
        }
        return render(request, 'posts/create_post.html', context)
    form.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post.objects.select_related('author', 'group'), id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    post = Post.objects.filter(author__following__user=request.user)
    page_obj = pagination(request, post)
    follow = True
    context = {
        'page_obj': page_obj,
        'follow': follow,
    }
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if request.user != author:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect('posts:profile', author)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    if request.user != author and Follow.objects.filter(
            user=request.user, author=author
    ).exists():
        Follow.objects.filter(user=request.user, author=author).delete()
    return redirect('posts:profile', author)


def search_post(request):
    query = request.GET.get('q')
    post = Post.objects.filter(Q(text__icontains=query))
    page_obj = pagination(request, post)
    context = {
        "page_obj": page_obj
    }
    return render(request, 'posts/search_match_post.html', context)
