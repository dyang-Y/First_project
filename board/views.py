from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import Post, Comment, Tag
from .forms import PostForm, CommentForm

# Create your views here.

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'board/post_list.html', {'posts': posts})

def tag_posts(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    posts = Post.objects.filter(tags=tag).order_by('-created_at')
    return render(request, 'board/tag_posts.html', {'tag': tag, 'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    comment_form = CommentForm()
    
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user.username
            comment.save()
            messages.success(request, '댓글이 등록되었습니다.')
            return redirect('post_detail', pk=post.pk)
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'board/post_detail.html', context)

@login_required(login_url='login')
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
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
        form = PostForm(request.POST, request.FILES, instance=post)
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

@login_required(login_url='login')
def comment_edit(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk, post__pk=post_pk)
    
    # 작성자만 편집 가능하도록 확인
    if comment.author != request.user.username:
        return HttpResponseForbidden("이 댓글을 편집할 권한이 없습니다.")
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, '댓글이 수정되었습니다.')
            return redirect('post_detail', pk=post_pk)
    else:
        form = CommentForm(instance=comment)
    
    return render(request, 'board/comment_form.html', {
        'form': form,
        'post_pk': post_pk,
        'comment_pk': comment_pk
    })

@login_required(login_url='login')
def comment_delete(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk, post__pk=post_pk)
    
    # 작성자만 삭제 가능하도록 확인
    if comment.author != request.user.username:
        return HttpResponseForbidden("이 댓글을 삭제할 권한이 없습니다.")
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, '댓글이 삭제되었습니다.')
        return redirect('post_detail', pk=post_pk)
    
    return render(request, 'board/comment_confirm_delete.html', {
        'comment': comment,
        'post_pk': post_pk
    })
