from django.shortcuts import render, redirect

from ideus.models import Question, Answer, Result
from .models import User
from django.contrib import auth

# Create your views here.
def mypage(request):
    user = User.objects.get(username=request.user)
    
    my_question = Question.objects.filter(userid = user.id).order_by('created_at')
    my_answer = Answer.objects.filter(userid = user.id).order_by('created_at')
    my_result = Result.objects.filter(userid = user.id).order_by('created_at')
    
    question_like = user.like_question.all()
    answer_like = user.like_answer.all()
    result_like = user.like_result.all()
    
    user = User.objects.get(id=user.id)
    return render(request, 'mypage.html', {
        'question_like': question_like,
        'answer_like': answer_like,
        'result_like': result_like,
        
        'my_question': my_question,
        'my_answer': my_answer,
        'my_result': my_result,
        'user':user
    })


def signup(request):
    if request.method == "POST":
        if request.POST["password1"] == request.POST["password2"]:
            user = User.objects.create_user(
                username=request.POST["username"], 
                password = request.POST["password1"])
            auth.login(request, user)
            return render(request, 'index.html')
        return render(request, 'signup.html')
    
    return render(request, 'signup.html')


def logout(request):
    response = render(request, 'index.html')
    response.delete_cookie('username')
    response.delete_cookie('password')
    auth.logout(request)
    return redirect('https://ideus.run.goorm.io')

def login(request):
    # 해당 쿠키에 값이 없을 경우 None을 return 한다.
    if request.COOKIES.get('username') is not None:
        username = request.COOKIES.get('username')
        password = request.COOKIES.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('https://ideus.run.goorm.io')
        else:
            return render(request, "login.html")

    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        # 해당 user가 있으면 username, 없으면 None
        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            if request.POST.get("keep_login") == "TRUE":
                response = redirect('/')
                response.set_cookie('username',username)
                response.set_cookie('password',password)
                return response
            return redirect('https://ideus.run.goorm.io')
        else:
            return render(request, 'login.html', {'error':'username or password is incorrect'})
    else:
        return render(request, 'login.html')
    return render(request, 'login.html') 