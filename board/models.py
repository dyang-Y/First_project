from django.db import models
from django.utils import timezone
import os

def get_upload_path(instance, filename):
    # 파일명이 중복되지 않도록 경로 설정: 'uploads/년/월/일/게시글ID_파일명'
    ymd_path = timezone.now().strftime('%Y/%m/%d')
    upload_path = os.path.join('uploads', ymd_path, filename)
    return upload_path

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    # 파일 업로드 필드 추가
    image = models.ImageField(upload_to=get_upload_path, blank=True, null=True)
    file = models.FileField(upload_to=get_upload_path, blank=True, null=True)
    
    def __str__(self):
        return self.title
    
    # 파일 확장자 반환 메서드
    def get_file_extension(self):
        if self.file:
            name, extension = os.path.splitext(self.file.name)
            return extension.lower()
        return None

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f'Comment by {self.author} on {self.post.title}'
