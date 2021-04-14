from django.shortcuts import render, redirect, get_object_or_404
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib import messages
from .models import Tag, Post
from .forms import PostForm, CommentForm

@login_required
def index(request):
    timesince = timezone.now() - timedelta(days=3)
    post_list = Post.objects.all()\
        .filter(
            Q(author=request.user) |
            Q(author__in=request.user.following_set.all())
        )\
        .filter(
            created_at__gte=timesince) # 3일이하 경과된 포스팅만 가져오겠다.

    suggested_user_list = get_user_model().objects.all().exclude(pk=request.user.pk)\
                            .exclude(pk__in=request.user.following_set.all())[:3]

    return render(request, "instagram/index.html", {
        'suggested_user_list': suggested_user_list,
        'post_list': post_list,
    })


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            post.tag_set.add(*post.extract_tag_list())
            messages.success(request, '포스팅을 저장했습니다.')
            return redirect(post)
    else:
        form = PostForm()
    
    return render(request, 'instagram/post_form.html', {'form': form, })


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "instagram/post_detail.html", {'post': post, })

@login_required
def comment_new(request, post_pk):
    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = get_object_or_404(Post, pk=post_pk)
            comment.author = request.user
            comment.save()
            messages.success(request, "댓글이 저장되었습니다.")
            return redirect(comment.post)
    else:
        form = CommentForm()
    return render(request, "instagram/comment_form.html", {'form': form,})


@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.like_user_set.add(request.user)
    messages.success(request, f"포스팅#{post.pk}를 좋아합니다.")
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)


@login_required
def post_dislike(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.like_user_set.remove(request.user)
    messages.success(request, f"포스팅#{post.pk}좋아요를 취소합니다.")
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)


def user_page(request, username):
    page_user = get_object_or_404(get_user_model(), username=username, is_active=True)

    if request.user.is_authenticated:
        is_follow = request.user.following_set.filter(pk=page_user.pk).exists()
    else:
        is_follow = False

    post_list = Post.objects.filter(author=page_user)
    post_list_count = post_list.count()
    return render(request, 'instagram/user_page.html', {
        'page_user': page_user, 
        'post_list': post_list,
        'post_list_count': post_list_count,
        'is_follow': is_follow,
        })


