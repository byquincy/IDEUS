from django.contrib import admin
# 추가작성 form
from .models import Question, Answer, Result

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Result)