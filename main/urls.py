from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('chat/', views.chat_page, name='chat'),
    path('chat/<int:conversation_id>/', views.chat_page, name='chat_conversation'),
    path('api/chat/', views.chat_api, name='chat_api'),
    path('recommendations/', views.recommendations_page, name='recommendations'),
    path('api/recommend/', views.recommend_api, name='recommend_api'),
    path('interview/', views.interview_page, name='interview'),
    path('api/interview/', views.interview_api, name='interview_api'),
    path('api/interview/submit/', views.interview_submit_api, name='interview_submit_api'),
    path('resume/', views.resume_page, name='resume'),
    path('resume/download/', views.resume_download, name='resume_download'),
    path('api/sentiment/', views.analyze_sentiment_api, name='analyze_sentiment_api'),
    path('cover-letter/', views.cover_letter_page, name='cover_letter'),
    path('api/cover-letter/', views.cover_letter_api, name='cover_letter_api'),
]
