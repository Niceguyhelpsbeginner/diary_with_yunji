from django.db import models
from django.core.validators import MinLengthValidator
from .validators import validate_symbols
from django.contrib.auth.models import AbstractUser

# Create your models here.
    
class Post(models.Model):
    # 글의 제목, 내용, 작성일, 마지막 수정일 
    title = models.CharField(max_length= 50, unique=True, error_messages={'unique': '중복되는 제목입니다.'})
    content = models.TextField(validators=[
                                        MinLengthValidator(10, '너무 짧아요, 10자이상 적어주세요!'), 
                                        validate_symbols
                                        ])
    dt_created = models.DateTimeField(verbose_name="Date Created", auto_now_add= True)
    dt_modified = models.DateTimeField(verbose_name= "Date Modified", auto_now = True)


    def __str__(self):
        return self.title

class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=30, unique=True)
    # 필요하다면 추가 필드 정의
    pass

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.nickname}: {self.content[:20]}"

