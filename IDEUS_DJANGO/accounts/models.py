from django.db import models
from ideus.models import Question, Answer, Result
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):  
    like_question = models.ManyToManyField(Question, blank=True)
    like_answer = models.ManyToManyField(Answer, blank=True)
    like_result = models.ManyToManyField(Result, blank=True)
    
    Introduction = models.CharField(max_length=100, blank=True, null=True)
    my_question = models.IntegerField(default=0)
    my_result = models.IntegerField(default=0)
    
    subject_like = models.CharField(default='dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd', max_length=100)