from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from .forms import SignUpForm
import re
from .models import UserProfile

# Create your views here.

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "회원가입이 완료되었습니다.")
            return redirect('post_list')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"{username}님, 환영합니다!")
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('post_list')
            else:
                messages.error(request, "로그인에 실패했습니다.")
        else:
            messages.error(request, "아이디 또는 비밀번호가 올바르지 않습니다.")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "로그아웃되었습니다.")
    return redirect('post_list')

def check_username(request):
    username = request.GET.get('username', '')
    is_taken = User.objects.filter(username=username).exists()
    is_valid = bool(re.match(r'^[a-zA-Z0-9@.+\-_]+$', username))
    return JsonResponse({
        'is_taken': is_taken,
        'is_valid': is_valid
    })

def check_nickname(request):
    nickname = request.GET.get('nickname', '')
    is_taken = UserProfile.objects.filter(nickname=nickname).exists()
    
    # 비속어 검사 (forms.py와 동일한 목록 사용)
    bad_words = [
        '바보', '멍청이', '병신', '개새끼', '씨발', '시발', '좆', '존나', '새끼',
        'babo', 'idiot', 'stupid', 'bastard', 'shit', 'fuck', 'asshole', 'damn'
    ]
    
    contains_bad_word = any(word.lower() in nickname.lower() for word in bad_words)
    
    is_valid = len(nickname) <= 15 and not contains_bad_word
    
    return JsonResponse({
        'is_taken': is_taken,
        'is_valid': is_valid,
        'contains_bad_word': contains_bad_word
    })
