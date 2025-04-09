from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
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