from django.urls import path

from . import views

#app_name = 'otp'

urlpatterns = [
    path('create', views.create, name='start'),
    path('start/<str:id_pub>', views.start, name='start'),
    path('quiz/<str:id_pub>/<int:question_seq>', views.quiz, name='start'),
    path('submit/<str:id_pub>', views.submit, name='submit_quiz'),
    path('create_dummy/<str:quiz_name>', views.create_dummy, name='create_dummy_quiz'),
    path('question_view/<str:key>/<int:qid>', views.question_view, name='question-view'),
    path('user_quiz_view/<str:id_pub>/<str:key>', views.user_quiz_view, name='user_quiz_view'),
    path('put_response/<str:id_pub>/<int:question_seq>', views.put_response, name='put_response'),
    path('flag_question/<str:id_pub>/<int:question_seq>', views.flag_question, name='flag_question'),
]