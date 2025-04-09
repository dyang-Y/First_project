from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Post
from .forms import PostForm

# Create your views here.

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'board/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'board/post_detail.html', {'post': post})

@login_required(login_url='login')
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user.username
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'board/post_form.html', {'form': form})

@login_required(login_url='login')
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # 작성자만 편집 가능하도록 확인
    if post.author != request.user.username:
        return HttpResponseForbidden("이 게시물을 편집할 권한이 없습니다.")
        
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'board/post_form.html', {'form': form})

@login_required(login_url='login')
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # 작성자만 삭제 가능하도록 확인
    if post.author != request.user.username:
        return HttpResponseForbidden("이 게시물을 삭제할 권한이 없습니다.")
        
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'board/post_confirm_delete.html', {'post': post})
