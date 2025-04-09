from django import forms
from django.utils.text import slugify
from .models import Post, Comment, Tag

class PostForm(forms.ModelForm):
    tag_input = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '쉼표로 구분하여 입력 (예: Django, Python, 웹개발)'}),
        label='태그',
        help_text='태그는 쉼표(,)로 구분하여 입력하세요.'
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': '제목',
            'content': '내용',
            'image': '이미지',
            'file': '첨부파일',
        }
        help_texts = {
            'image': '이미지 파일(jpg, png, gif 등)을 업로드하세요',
            'file': '문서 파일(pdf, docx, xlsx 등)을 업로드하세요',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 편집 시 기존 태그를 표시
        if self.instance.pk:
            existing_tags = self.instance.tags.all()
            if existing_tags:
                self.initial['tag_input'] = ', '.join([tag.name for tag in existing_tags])
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if commit:
            instance.save()
            # 태그 처리
            if self.cleaned_data.get('tag_input'):
                # 기존 태그 연결 제거
                instance.tags.clear()
                # 새 태그 분리 및 저장
                tag_names = [tag.strip() for tag in self.cleaned_data['tag_input'].split(',') if tag.strip()]
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    instance.tags.add(tag)
            
            self.save_m2m()
        
        return instance

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '댓글을 입력하세요...'}),
        }
        labels = {
            'content': '댓글',
        } 