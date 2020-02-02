from django import forms
from .models import Answer, Question, Result

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('title', 'content', 'photo')
        
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('title', 'content', 'subject', 'photo')
                  
class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ('title', 'link', 'content',)