from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin

admin.site.register(User, UserAdmin)

class CustomUserAdmin(UserAdmin):
    # fieldsets : 관리자 리스트 화면에서 출력될 폼 설정 부분
    UserAdmin.fieldsets[1][1]['fields']+=('Introduction', 'like_question','like_answer','like_result', 'my_question', 'my_result', 'subject_like')
    # add_fieldsets : User 객체 추가 화면에 출력될 입력 폼 설정 부분
    UserAdmin.add_fieldsets += (
        (('Additional Info'),{'fields':('Introduction', 'like_question','like_answer','like_result', 'my_question', 'my_result', 'subject_like')}),
    )