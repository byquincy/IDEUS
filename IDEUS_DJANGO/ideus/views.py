from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q

from IDEUS_DJANGO.constants import SUBJECT_CHOICES, SUBJECT_DICT
from accounts.models import User
from .models import Question, Answer, Result
from .forms import AnswerForm, QuestionForm, ResultForm
#index page
def index(request):
    waiting_question = Question.objects.filter(answers = 0).order_by('created_at')
    answer_question = Question.objects.filter(~Q(answers = 0)).order_by('created_at')
    return render(request, 'index.html', {
        'waiting_question': waiting_question,
        'answer_question': answer_question
    })

def user_detail(request, user_id):
    detail_user = get_object_or_404(User, id=user_id)
    user_answer = Answer.objects.filter(userid = detail_user.id).order_by('created_at')
    user_result = Result.objects.filter(userid = detail_user.id).order_by('created_at')
    
    like_subject = list()
    for i in detail_user.subject_like:
        like_subject.append(ord(i))
    like_subject[0] = 0
    favorite_subject = SUBJECT_DICT[like_subject.index(max(like_subject))]
        
    return render(request, 'user_detail.html', {
        'detail_user':detail_user,
        'user_answer':user_answer,
        'user_result':user_result,
        'favorite_subject': favorite_subject,
    })

def model_list(request, modeltype, list_subject, sorting):
    user = request.user
    
    if sorting == 'mylikes':    #내가 좋아한질문은 유저에서 불러와야하므로 예외
        if modeltype == 'question':
            result_list = user.like_question.order_by('-created_at')
            title = '질문'
        elif modeltype == 'answer':
            result_list = user.like_answer.order_by('-created_at')
            title = '답변'
        elif modeltype == 'result':
            result_list = user.like_result.order_by('-created_at')
            title = '결과물'
    elif modeltype == 'question':    #질문일경우
        result_list = Question.objects.all()
        title = '질문'
        #질문만 쓸수있는 정렬기준
        if sorting == 'manyanswer':
            result_list = result_list.order_by('-answers', '-created_at')
            title = '모든 질문'
        elif sorting == 'existanswer':
            result_list = result_list.filter(~Q(answers = 0)).order_by('-created_at')
            title = '아이디어를 받은 질문'
        elif sorting == 'noanswer':
            result_list = result_list.filter(answers = 0).order_by('-created_at')
            title = '아이디어를 기다리는 질문'
    elif modeltype == 'answer':        #답변일경우
            result_list = Answer.objects.all()
            title = '답변'
    elif modeltype == 'result':        #결과물일경우
            result_list = Result.objects.all()
            title = '결과물'
        
    #주제 선택
    if list_subject != 'all':    #all이면 필요없음
        list_subject = int(list_subject)    #정수형으로 변환
        if modeltype == 'question':
            result_list = result_list.filter(subject=list_subject)
            
    #정렬방식 선택
    if sorting == 'mylikes':    #mylikes는 이미 정렬했으므로 할필요없음
        title = '내가 좋아한 ' + title
    elif sorting == 'my':
        result_list = result_list.filter(userid=user.id)
        title = '내가 쓴 ' + title
    elif sorting == 'newest':   #모두해당하지 않을경우 기본(최신순)정렬
        result_list = result_list.order_by('-created_at')
        title = '모든 ' + title
    elif sorting == 'manylike':
        result_list = result_list.order_by('-like', '-created_at')
        title = '모든 ' + title
    elif modeltype == 'answer' or modeltype == 'result':
        return redirect('model_list', modeltype, list_subject, 'newest')
    
    #결과물 적용
    paginator = Paginator(result_list, 10)
    page = request.GET.get('page')
    pageposts = paginator.get_page(page)
    
    return render(request, modeltype + '_list.html', {
        'result_list': result_list,
        'pageposts': pageposts,
        'title': title,
        'subject': list_subject,
        'subject_dict': SUBJECT_DICT.items(),
        'sorting': sorting,
    })

def question_detail(request, pk):
    question = Question.objects.get(pk=pk)
    
    return render(request, 'question_detail.html', {
        'question': question,
    })

def result_new(request, pk):
    if not request.user.is_active:
        return redirect('question_detail', pk)
    
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=request.user)
            result = form.save()
            
            result.question = Question.objects.get(pk=pk)
            result.username = user.username
            result.userid = user.id
            user.my_result += 1
            if 'youtu' in result.link:
                result.link = 'https://www.youtube.com/embed/' + result.link[-11:]
            if 'vimeo' in result.link:
                result.link = 'https://player.vimeo.com/video/' + result.link[-9:] + '?title=0&byline=0&portrait=0'
            
            user.save()
            result.save()
            return redirect('question_detail', pk)
        else:
            messages.info(request, '필수값을 모두 입력해주세요')
            
    else:
        form = ResultForm()
    return render(request, 'result_form.html', {
        'form' : form,
    })

def answer_new(request, pk):
    if not request.user.is_active:
        return redirect('question_detail', pk)
    
    if request.method == 'POST':
        form = AnswerForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.get(username=request.user)
            question = Question.objects.get(pk=pk)
            answer = form.save()
            
            answer.question = Question.objects.get(pk=pk)
            answer.username = user.username
            answer.userid = user.id
            question.answers += 1
            user.subject_like = user.subject_like[:question.subject] + chr(ord(user.subject_like[question.subject])+2) + user.subject_like[question.subject+1:]
            
            user.save()
            question.save()
            answer.save()
            return redirect('question_detail', pk)
        else:
            messages.info(request, '필수값을 모두 입력해주세요')
    else:
        form = AnswerForm()
    
    return render(request, 'answer_form.html', {
        'form' : form,
    })

def question_new(request):
    if not request.user.is_active:
        return redirect('question_detail', pk)
    
    if request.method == "POST":
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.get(username=request.user)
            question = form.save()
            
            question.username = user.username
            question.userid = user.id
            user.my_question += 1
            user.subject_like = user.subject_like[:question.subject] + chr(ord(user.subject_like[question.subject])+3) + user.subject_like[question.subject+1:]
            
            user.save()
            question.save()
            return redirect('question_detail', question.id)
        else:
            messages.info(request, '필수값을 모두 입력해주세요')
    else:
        form = QuestionForm()
        return render(request, 'question_form.html', {
            'form' : form,
            'subject': SUBJECT_DICT.items(),
        })

def question_like(request, pk):
    if not request.user.is_active:
        return redirect('question_detail', pk)
    
    question = get_object_or_404(Question, id=pk)
    user = User.objects.get(username=request.user)
    if user.like_question.filter(id=pk).exists():
        user.like_question.remove(question)
        user.subject_like = user.subject_like[:question.subject] + chr(ord(user.subject_like[question.subject])-1) + user.subject_like[question.subject+1:]
        question.like -= 1
    else:
        user.like_question.add(question)
        user.subject_like = user.subject_like[:question.subject] + chr(ord(user.subject_like[question.subject])+1) + user.subject_like[question.subject+1:]
        question.like += 1
    
    user.save()
    question.save()
    return redirect('question_detail', pk)

def answer_like(request, pk):
    if not request.user.is_active:
        return redirect('question_detail', answer.question.id)
    
    answer = get_object_or_404(Answer, id=pk)
    user = User.objects.get(username=request.user)
    if user.like_answer.filter(id=pk).exists():
        user.like_answer.remove(answer)
        answer.like -= 1
    else:
        user.like_answer.add(answer)
        answer.like += 1
    answer.save()
    return redirect('question_detail', answer.question.id)

def result_like(request, pk):
    if not request.user.is_active:
        return redirect('question_detail', result.question.id)
    
    result = get_object_or_404(Result, id=pk)
    user = User.objects.get(username=request.user)
    if user.like_result.filter(id=pk).exists():
        user.like_result.remove(result)
        result.like -= 1
    else:
        user.like_result.add(result)
        result.like += 1
    result.save()
    return redirect('question_detail', result.question.id)