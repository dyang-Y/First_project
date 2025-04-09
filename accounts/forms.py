from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re
from django.core.exceptions import ValidationError

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
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # 영문자, 숫자, 특수문자(@/./+/-/_)만 허용하는 정규식
        if not re.match(r'^[a-zA-Z0-9@.+\-_]+$', username):
            raise ValidationError('사용자명은 영문자, 숫자, 특수문자(@/./+/-/_)만 사용 가능합니다. 한글이나 다른 특수문자는 사용할 수 없습니다.')
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        # 한글, 영문자만 허용하는 정규식
        if not re.match(r'^[가-힣a-zA-Z\s]+$', first_name):
            raise ValidationError('이름은 한글과 영문자만 입력 가능합니다. 숫자나 특수문자는 사용할 수 없습니다.')
        return first_name
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        if commit:
            user.save()
        return user 