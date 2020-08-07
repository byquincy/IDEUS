from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.index, name='index'),
    
    path('list/<modeltype>/<list_subject>/<sorting>/', views.model_list, name='model_list'),
    
    
    path('question/<int:pk>/', views.question_detail, name='question_detail'),
    path('question/<int:pk>/delete', views.question_delete, name='question_delete'),
 
    path('new/question/', views.question_new, name='question_new'),
    path('new/answer/<int:pk>/', views.answer_new, name='answer_new'),
    path('new/result/<int:pk>/', views.result_new, name='result_new'),
    
    path('like/question/<int:pk>/', views.question_like, name='question_like'),
    path('like/answer/<int:pk>/', views.answer_like, name='answer_like'),
    path('like/result/<int:pk>/', views.result_like, name='result_like'),
    
    path('user/<int:user_id>/', views.user_detail, name='user_detail'),

]
