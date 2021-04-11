from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Tag
from .forms import PostForm

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
            return redirect('/')
    else:
        form = PostForm()
    
    return render(request, 'instagram/post_form.html', {'form': form, })