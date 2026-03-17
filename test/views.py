import json, requests
from django.shortcuts import render,get_object_or_404,redirect
from datetime import timedelta,datetime,timezone
from . import settings as quiz_settings
from django.http import HttpResponse, Http404
from assessment.models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required


# This function should never be called from AJAX, because it will expose the client key
# It expects the following  POST parameters
# api_key
# forward_url - URL after successful verification
# update_url  - POST to this url before forwarding. Client should match the key for security
# var (Optional)  = An optional var parameter which will be passed back in update_url POST
@csrf_exempt
def create(request):
    # Raise error if any of the mandatory parameters is missing
    try:
        api_key = request.POST['api_key']
        update_url = request.POST['update_url']
        forward_url = request.POST['forward_url']
        quiz_name = request.POST['quiz_name']
    except KeyError:
        return HttpResponse('Error: Missing one or more parameters')
    var = request.POST.get('var') # Will return None if var is not there
    try:
        client = Client.objects.get(api_key=api_key)
    except(Client.DoesNotExist):
        raise Http404("Error: Client API key does not exist")

    if client.is_active is False:
        return HttpResponse('The client is is not active. Please contact customer service')

    user_quiz = __create_quiz(client,quiz_name,forward_url)
    user_quiz.update_url = update_url
    if var is not None:
        user_quiz.var = var
    user_quiz.save()
    quiz_url = quiz_settings.QUIZ_BASE_URL + user_quiz.id_pub
    response = {'quiz_url':quiz_url,'key':user_quiz.key,'created_at':str(user_quiz.created_at)}
    return HttpResponse(json.dumps(response))

# This function will create dummy quiz
# Client ID 1 is dummy clinet for testing the quizzes
@staff_member_required
def create_dummy(request,quiz_name):
    forward_url = ''
    client = Client.objects.get(api_key = quiz_settings.DUMMY_CLIENT_KEY)
    user_quiz = __create_quiz(client,quiz_name,forward_url)
    user_quiz.forward_url = '/assessment/user_quiz_view/' + user_quiz.id_pub + '/' + user_quiz.key
    user_quiz.save()
    quiz_url = quiz_settings.QUIZ_BASE_URL + user_quiz.id_pub
    return redirect(quiz_url)


def __create_quiz(client,quiz_name,forward_url):
    # Now create a UserQuiz.
    quiz = Quiz.objects.get(name=quiz_name)
    user_quiz = UserQuiz.objects.create(client=client,quiz=quiz, forward_url=forward_url)
    # Create QuizResponses and calculate number of questions
    qcs = quiz.quizconcept_set.all()
    questions = []
    for qc in qcs:
        questions += list(qc.concept.questionbank_set.all().order_by('?')[:qc.num_questions])
    # Now create response objects for each question and save them in db
    sequence = 0
    for q in questions:
        response = QuizResponse(user_quiz=user_quiz)
        sequence += 1
        response.sequence = sequence
        response.question = q
        response.save()
    user_quiz.num_questions = sequence
    user_quiz.save()
    return user_quiz

def start(request,id_pub):
    user_quiz = UserQuiz.objects.get(id_pub=id_pub)
    # Submit the question if the quiz expired
    # TODO - Sumbit if the quiz is expired
    # If already submitted, throw 404
    if user_quiz.expires_at is not None:
        if datetime.now(timezone.utc) > user_quiz.expires_at:
            if user_quiz.submitted_at is None:
               return redirect('/assessment/submit/' + id_pub)
            else:
                raise Http404('This quiz has expired')
    quiz_url = 'assessment/quiz/'+id_pub+'/1'
    context = {'quiz_url':quiz_url,'id_pub':id_pub, 'user_quiz':user_quiz}
    return render(request, 'assessment/start.html', context)


def question_view(request,key,qid):
    if key != quiz_settings.VIEW_KEY:
        return Http404('Wrong Key')
    question = QuestionBank.objects.get(id=qid)
    options = question.questionbankoption_set.all()
    meta = {'title':'Question View | flipClass.com'}
    context = {'question':question,'options':options,'meta':meta}
    return render(request, 'assessment/question_view.html', context)

def user_quiz_view(request,id_pub,key):
    uq = UserQuiz.objects.get(id_pub=id_pub)
    if uq.key != key:
        raise Http404('Invalid Key')
    responses = QuizResponse.objects.filter(user_quiz=uq)
    meta = {'title': 'Quiz View | flipClass.com'}
    context = {'responses': responses, 'meta':meta}
    return render(request, 'assessment/user_quiz_view.html', context)


# Quiz
def quiz(request,id_pub,question_seq):
    user_quiz = UserQuiz.objects.get(id_pub=id_pub)
    if user_quiz.submitted_at is not None:
        raise Http404('This quiz has been submitted.')
    if question_seq > user_quiz.num_questions or question_seq <= 0:
        return Http404('Error! Question does not exist')
    # If quiz started then set start and expiry time
    if question_seq == 1 and user_quiz.started_at is None:
        user_quiz.started_at = datetime.now(timezone.utc)
        user_quiz.expires_at = datetime.now(timezone.utc) + timedelta(minutes=user_quiz.quiz.time_min)
        user_quiz.save()

    question = user_quiz.quizresponse_set.get(sequence=question_seq).question
    options = QuestionBankOption.objects.filter(question=question).order_by('sequence')
    responses = QuizResponse.objects.filter(user_quiz=user_quiz)
    current_response = QuizResponse.objects.get(user_quiz=user_quiz,sequence=question_seq)
    previous=0
    next = 0
    if question_seq < user_quiz.num_questions:
        next = question_seq + 1
    if question_seq > 1:
        previous = question_seq - 1
    meta = {'title':'flipClass Quiz | ' + user_quiz.quiz.display_name}
    expiry_string = user_quiz.expires_at.strftime("%Y-%m-%dT%H:%M:%S")+'Z'
    qdict = {'question':question,'options':options,'responses':responses,'seq':question_seq,'user_quiz':user_quiz,'next':next, 'previous':previous,'current_response':current_response,'expiry_dt':expiry_string,}
    context = {'meta':meta,'qdict':qdict}
    return render(request, 'assessment/quiz.html', context)

# Capture responses through jQuery
def put_response(request,id_pub,question_seq):
    quiz = UserQuiz.objects.get(id_pub=id_pub)
    if question_seq > quiz.num_questions or question_seq <= 0:
        raise Http404('Error! Question does not exist')
    # TODO - if quiz is expired then submit
    if quiz.expires_at < datetime.now(timezone.utc):
        raise Http404("Time over! Please submit the quiz")
    resp_opt = int(request.GET['option'])
    question = QuizResponse.objects.get(user_quiz=quiz, sequence=question_seq)
    question.selected_index = resp_opt
    question.submitted_at = datetime.now(timezone.utc)
    question.save()
    return HttpResponse('Option recorded')

# Capture responses through jQuery
def flag_question(request,id_pub,question_seq):
    user_quiz = UserQuiz.objects.get(id_pub=id_pub)
    if question_seq > user_quiz.num_questions or question_seq <= 0:
        return Http404('Error! Question does not exist')
    # TODO - if quiz expired then submit
    question = QuizResponse.objects.get(user_quiz=user_quiz, sequence=question_seq)
    question.is_flagged = not question.is_flagged
    question.save()
    return HttpResponse('Question Flagged')

# When a UserQuiz is submitted, calculate score and post to update_url
def submit(request,id_pub):
    # If it is submitted, then just forward to the url
    user_quiz = UserQuiz.objects.get(id_pub=id_pub)
    if user_quiz.submitted_at:
        return redirect(user_quiz.forward_url)
    else:
        responses = QuizResponse.objects.filter(user_quiz=user_quiz)
        num_correct=0
        for resp in responses:
            if resp.selected_index is not None:
                opt = QuestionBankOption.objects.get(question=resp.question, sequence=resp.selected_index)
                if opt.is_correct:
                    resp.is_correct = True
                    num_correct += 1
                else:
                    resp.is_correct = False
            else:
                # User has not selected any option
                resp.is_correct = False
            resp.save()
        user_quiz.num_correct = num_correct
        user_quiz.submitted_at = datetime.now(timezone.utc)
        user_quiz.save()
        # Update if the update_url is defined
        if user_quiz.update_url is not None:
            # Now post the quiz result at update url
            test_data = {'key':user_quiz.key,'score':num_correct,'total':user_quiz.num_questions}
            resp = requests.post(user_quiz.update_url, data=test_data)
        # Forward to url
        return redirect(user_quiz.forward_url)
    return None
# Calculate score and return json response


