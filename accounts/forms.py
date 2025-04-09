from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re
from django.core.exceptions import ValidationError

# 연속된 문자/숫자를 체크하는 함수
def contains_consecutive_chars(value, length=3):
    # 숫자 연속성 체크
    for i in range(10 - length + 1):
        consecutive_nums = ''.join(map(str, range(i, i + length)))
        if consecutive_nums in value:
            return True
        
        # 역순 체크
        reverse_nums = ''.join(map(str, range(i + length - 1, i - 1, -1)))
        if reverse_nums in value:
            return True
            
    # 알파벳 연속성 체크
    for i in range(26 - length + 1):
        # 소문자 연속성
        consecutive_chars = ''.join(chr(ord('a') + j) for j in range(i, i + length))
        if consecutive_chars in value.lower():
            return True
            
        # 역순 체크
        reverse_chars = ''.join(chr(ord('a') + j) for j in range(i + length - 1, i - 1, -1))
        if reverse_chars in value.lower():
            return True
            
    return False

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='실명을 입력해주세요. 한글과 영문자만 사용 가능합니다.'
    )
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Form 필드에 부트스트랩 클래스 추가
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        # 사용자명 필드에 도움말 추가
        self.fields['username'].help_text = '영문자, 숫자, 특수문자(@/./+/-/_)만 사용 가능합니다. 한글은 사용할 수 없습니다.'
        # 비밀번호 확인 필드 라벨 명확하게
        self.fields['password2'].label = '비밀번호 확인'
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # 영문자, 숫자, 특수문자(@/./+/-/_)만 허용하는 정규식
        if not re.match(r'^[a-zA-Z0-9@.+\-_]+$', username):
            raise ValidationError('사용자명은 영문자, 숫자, 특수문자(@/./+/-/_)만 사용 가능합니다. 한글이나 다른 특수문자는 사용할 수 없습니다.')
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        # 한글, 영문자만 허용하는 정규식 (공백 제외)
        if not re.match(r'^[가-힣a-zA-Z]+$', first_name):
            raise ValidationError('이름은 한글과 영문자만 입력 가능합니다. 숫자나 특수문자, 공백은 사용할 수 없습니다.')
        return first_name
        
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        
        # 연속된 문자/숫자 체크
        if contains_consecutive_chars(password1, 3):
            raise ValidationError('연속된 3개 이상의 숫자나 문자(예: 123, abc)는 비밀번호로 사용할 수 없습니다.')
        
        return password1

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        if commit:
            user.save()
        return user 