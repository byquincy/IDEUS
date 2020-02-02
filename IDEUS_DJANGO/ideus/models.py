from django.db import models
from IDEUS_DJANGO.constants import SUBJECT_CHOICES

#질문 모델
class Question(models.Model):
    username = models.CharField(max_length = 24)
    userid = models.IntegerField(null=True)
    
    title = models.CharField(max_length=100)
    content = models.TextField()
    photo = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    like = models.IntegerField(default=0)
    subject = models.IntegerField(default=0, choices=SUBJECT_CHOICES)
    answers = models.IntegerField(default=0)
def __str__(self):
    return self.title

#댓글 모델
class Answer(models.Model):
    username = models.CharField(max_length = 24)
    userid = models.IntegerField(null=True)
    
    question = models.ForeignKey('Question', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    photo = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    like = models.IntegerField(default=0)
def __str__(self):
    return self.title

#결과물 공유
class Result(models.Model):
    username = models.CharField(max_length = 24)
    userid = models.IntegerField(null=True)
    
    question = models.ForeignKey('Question', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.URLField()
    
    like = models.IntegerField(default=0)
def __str__(self):
    return self.title