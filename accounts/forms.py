from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re
from django.core.exceptions import ValidationError

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
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
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user 