from random import shuffle
from django.db.utils import Error
from django.http import HttpRequest, HttpResponseRedirect
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Avg
from django.db.models.aggregates import Count
from django.db.models.expressions import F

from .models import Answer, User, Quiz, Question, Topic, Participant, ParticipantAnswer, Option, ErrorMessage
import json
from random import shuffle
from .utils import grading
from datetime import datetime



def index(request):

  if request.method == "POST":
    # error message from users
    message = request.POST.get('message')
    email = request.POST.get('email')
    errM = ErrorMessage(message=message, email=email)
    errM.save()

  topics = Topic.objects.annotate(fieldsum = Count('quizzes')).order_by('-fieldsum').all()
  # output: queryset of topics but may not giving a list with each topic unique with each other. So not distinct yet

  unique_topics = [topics[0]]
  for topic in topics:
    # if topic.id is not in a list of unique_topics, differentiated by their ids.
    if topic.id not in [topic.id for topic in unique_topics] and len(unique_topics) <= 8:
      unique_topics.append(topic)

  contributors = [user for user in User.objects.annotate(contrib_count = Count('quizzes')).order_by('-contrib_count') if user.has_contribution()]

  return render(request, "quizApp/index.html", {
    "Topics": unique_topics[0:8],
    "Contributors": contributors[0:6],
  })
  # return HttpResponse('Start of Quiz App')


def login_view(request):
  if request.method == "POST":

      # Attempt to sign user in
      username = request.POST["username"]
      password = request.POST["password"]
      user = authenticate(request, username=username, password=password)

      # Check if authentication successful
      if user is not None:
          login(request, user)
          return HttpResponseRedirect(reverse("index"))
      else:
          return render(request, "quizApp/login.html", {
              "message": "Invalid username and/or password."
          })
  else:
      return render(request, "quizApp/login.html")


def logout_view(request):
  logout(request)
  return HttpResponseRedirect(reverse("index"))


def register(request):
  if request.method == "POST":
      username = request.POST["username"]
      email = request.POST["email"]

      # Ensure password matches confirmation
      password = request.POST["password"]
      confirmation = request.POST["confirmation"]
      if password != confirmation:
          return render(request, "quizApp/register.html", {
              "message": "Passwords must match."
          })

      # Attempt to create new user
      try:
          user = User.objects.create_user(username, email, password)
          user.save()
      except IntegrityError:
          return render(request, "quizApp/register.html", {
              "message": "Username already taken."
          })
      login(request, user)
      return HttpResponseRedirect(reverse("index"))
  else:
      return render(request, "quizApp/register.html")


@login_required(login_url='login')
def profile(request, username):
  # return HttpResponse(Quiz.objects.get(id=2).testAvg())
  # return HttpResponse(Participant.objects.filter(quiz__id=2).aggregate(Avg('score')).values())
  user = User.objects.get(username=username)
  my_quizzes = Quiz.objects.filter(creator__username=username)
  following_quizzes = Quiz.objects.filter(creator__in=user.follows.all())
  topics = Topic.objects.all()

  try:
    # if the account is followed by the user
    user.followers.get(id=request.user.id)
    follow_status = True
  except:
    follow_status = False

  if request.method == "POST":
    # changing profile picture
    # return JsonResponse(request.POST, safe=False)
    # return JsonResponse(request.FILES.get('image')==None, safe=False)
    if request.FILES.get('image') != None:
      img = request.FILES.get('image')
      user.image = img

    # change status
    if request.POST.get('status') != None:
      status = request.POST.get('status')
      user.level = status

    user.save()

    # Re-Query
    user = User.objects.get(username=username)

  contributions = []
  for topic in topics:
    if Quiz.objects.filter(creator__username=username, topic=topic).count() != 0:
      contributions.append((topic.title, Quiz.objects.filter(creator__username=username, topic=topic).count()))

  return render(request, "quizApp/profile.html", {
    "User": user,
    "myQuizzes": my_quizzes,
    "followingQuizzes": following_quizzes,
    "Contributions": contributions,
    "Follow_status": follow_status,
  })


@login_required(login_url='login')
def follow(request, username):
  account = User.objects.get(username=username)
  try:
    # Check whether the user already follows the account or not
    User.objects.get(username=username, followers=request.user)
    account.followers.remove(request.user)
  except:
      # if the user hasn't followed the account
      account.followers.add(request.user)

  return HttpResponseRedirect(reverse('profile', args=[username]))


@login_required(login_url='login')
def study(request):
  
  topics = Topic.objects.all().order_by('title').all()
  # print(request.GET.get('study-search'))
  if request.method == "GET" and request.GET.get('study-search') != None:
    search = request.GET.get('study-search')
    search_topic = []
    for topic in topics:
      # print(f'check whether {search} is in {topic.title.lower()}')
      if search.lower() in topic.title.lower():
        search_topic.append(topic)
    topics = search_topic

  return render(request, "quizApp/study.html", {
    "Topics": topics
  })


@login_required(login_url='login')
def topic(request, topic_id, topic_slug):
  quizzes = Quiz.objects.filter(topic__id=topic_id, topic__slug=topic_slug).order_by('-date').all()
  # Quiz.objects.filter(topic__id=topic_id, topic__slug=topic_slug, taken_by__in=Participant.objects.filter())

  q = []
  for quiz in quizzes:
    if request.user.is_authenticated:
      # authenticated user
      participant = Participant.objects.filter(user=request.user, quiz=quiz).aggregate(Avg('score'))['score__avg']
      if participant != None:
        # if the use has attempted the quiz at least once, average the user's score
        has_been_taken_or_score = participant
      else:
        # if the user hasn't made any attempt at the quiz
        has_been_taken_or_score = False
    else:
      # anonymous user
      has_been_taken_or_score = False
    q.append((quiz, has_been_taken_or_score))
  # q = ( ( <Query Object>, has_been_taken_by_the_user_status (True/False value) ) )

  if request.GET.get('search-quiz') != None:
    search = request.GET.get('search-quiz')
    search_result = []
    for query_obj, status in q:
      if search.lower() in query_obj.title.lower():
        search_result.append((query_obj, status))
    q = search_result

  return render(request, "quizApp/topic.html", {
    "Topic": Topic.objects.get(id=topic_id),
    "Quizzes": q,
  })


@login_required(login_url='login')
def test(request, quiz_id, quiz_slug):

  quiz = Quiz.objects.get(id=quiz_id, slug=quiz_slug)
  questions = quiz.questions.all()

  # save participant data
  participant = Participant(user=request.user, quiz=quiz, time_start=datetime.now(), time_finished=datetime.now(), score=0)
  participant.save()

  # questions navigation
  questions_length = [number for number in range(1, len(questions)+1)]

  # reconstruct
  questions_for_nav = {}
  for number in questions_length:
    questions_for_nav[number] = ""
  for number in  range(0, len(questions)):
    questions_for_nav[number+1] = questions[number].id
  # output {
  #   question_number: question.id,
  #   question_number: question.id,
  #                 1: 2,
  #                 2: 4,
  #                 3: 5,
  #             etc...
  # }

  data_q = []
  for number in questions_length:
    # print(number);
    data_q.append((number, questions[number-1]))

  return render(request, "quizApp/test.html", {
    "Quiz": quiz,
    "Participant": participant,
    # "Questions": page_obj,
    "Questions": data_q,
    "Questions_Length": questions_for_nav,
  })


# def answers(request, quiz_id, quiz_slug, participant_id):

#   participant = Participant.objects.get(id=participant_id, user=request.user, quiz__id=quiz_id)
#   quiz = Quiz.objects.get(id=quiz_id)
#   questions = quiz.questions.all()

#   questions_length = [number for number in range(1, len(questions)+1)]

#   questions_for_nav = {}
#   for number in questions_length:
#     questions_for_nav[number] = ""
#   for number in  range(0, len(questions)):
#     questions_for_nav[number+1] = questions[number].id
#   # output: questions_for_nav = {number of a question: question.id, number of a question: question.id, ...}
  
#   if request.method == "POST":

#     # save the finished date
#     participant.time_finished = datetime.now()
#     participant.save()

#     # delete pre-existing records
#     ParticipantAnswer.objects.filter(participant = participant).delete()

#     for number, question_id in questions_for_nav.items():

#       # query the question
#       question = Question.objects.get(id=question_id)
#       # take the answer
#       answer = request.POST.get(f'{question_id}')
#       if answer == None: # answer is Null
#         answer = ""
#       # save it into the model
#       data = ParticipantAnswer(participant=participant, question=question, answer=answer)
#       data.save()

#     # grading score ( I feel there is a better way to do this )
#     grading(request=request, participation_id = participant.id, questions=questions, participant_answers=participant.answers.all() )

#     # updating quiz' average score
#     ## TURNS OUT NOT REALLY NEEDED. JUST USE METHOD OF THE MODEL
#     # avg = Participant.objects.filter(quiz=quiz).aggregate(Avg('score')).values()
#     # update_avg = Quiz(average_score=avg)
#     # update_avg.save()
    
#     # RE-Query ParticipantAnswer after the answers has been saved and answers has been graded (scored).
#     participant = Participant.objects.get(id=participant_id, user=request.user, quiz__id=quiz_id)
#     quiz = Quiz.objects.get(id=quiz_id)
#     questions = quiz.questions.all()

#   # questions_status_answers_and_options = {}
#   # true_false = {}
#   # answers_and_options = {}
#   # options = []
#   # for nomor in range(0, len(questions)):
#   #   # return HttpResponse(questions[4].options.all()[3].option)
#   #   for number in range(0, len(questions)):
#   #     options.append( questions[nomor].options.all()[number].option )
#   #   if participant.answers.all()[nomor].answer == questions[nomor].answer.all()[0].answer:
#   #     status = True
#   #   else:
#   #     status = False
#   #   answers_and_options[f"{participant.answers.all()[nomor].answer}"] = options
#   #   true_false[status] = answers_and_options
#   #   questions_status_answers_and_options[f"{questions[nomor]}"] = true_false
#   #   true_false = {}
#   #   answers_and_options = {}
#   #   options = []
  
#   # for easier query about answer correctness highlighting in the template.
#   for question in questions:
#     question.number = participant_id
#     question.save()

#   return render(request, "quizApp/answers.html", {
#     "Participant": participant,
#     "Quiz": quiz,
#     "Questions": questions,
#     "Questions_Length": questions_for_nav,
#     # "Questions_Status_Answers_and_Options": questions_status_answers_and_options,
#   })


@login_required(login_url='login')
def answers(request, quiz_id, quiz_slug, participant_id):

  participant = Participant.objects.get(id=participant_id)
  quiz = Quiz.objects.get(id=quiz_id, taken_by__id=participant_id)
  questions = quiz.questions.all()
  
  questions_length = [number for number in range(1, len(questions)+1)]

  questions_for_nav = {}
  for number in questions_length:
    questions_for_nav[number] = ""
  for number in  range(0, len(questions)):
    questions_for_nav[number+1] = questions[number].id

  if request.method == "POST":
    
    participant.time_finished = datetime.now()
    participant.save()

    # delete pre-existing records
    ParticipantAnswer.objects.filter(participant = participant).delete()

    for number, question_id in questions_for_nav.items():

      # query the question
      question = Question.objects.get(id=question_id)
      # take the answer
      answer = request.POST.get(f'{question_id}')
      if answer == None: # answer is Null
        answer = ""
      # save it into the model
      data = ParticipantAnswer(participant=participant, question=question, answer=answer)
      data.save()

    grading(request=request, participation_id = participant.id, questions=questions, participant_answers=participant.answers.all() )

    # RE-Query ParticipantAnswer after the answers has been saved and answers has been graded (scored).
    participant = Participant.objects.get(id=participant_id)
    quiz = Quiz.objects.get(id=quiz_id, taken_by__id=participant_id)
    questions = quiz.questions.all()

  
  data_q = []
  for number in questions_length:
    # print(number);
    data_q.append((number, questions[number-1]))

  return render(request, "quizApp/answers.html", {
    "Quiz": quiz,
    "Participant": participant,
    "Questions": data_q,
    "Questions_Length": questions_for_nav,
  })


@login_required(login_url='login')
def make_quiz(request, username):

  # query Topics
  topics = Topic.objects.all()

  if request.user.username != username:
    
    # message = 'You can only make a quiz for yourself.'
    return HttpResponseRedirect(reverse("make_quiz", args=[request.user.username]))

  if request.method == "POST":

    # return JsonResponse((request.POST), safe=False)

    # save the quiz data
    title = request.POST.get('title')
    if title == "" or title == None:
      return HttpResponse('error Title Not Defined')
    topic = request.POST.get('topic')
    topic = Topic.objects.get(title=topic)
    slug = title.replace(' ', '-')
    quiz = Quiz(slug=slug, title=title, creator=request.user, topic=topic)
    quiz.save()

    # save the question data
    number_of_questions = int(request.POST.get('num'))
    for number in range(1, number_of_questions+1):
      question = request.POST.get(f'q-{number}')
      q = Question(quiz=quiz, question=question)
      q.save()

      # save the options data
      # number_of_options = request.POST.get(f'q-{number}-opt-num')
      number_of_options = 5 # 5 options
      for option in range(1, number_of_options+1):
        option = request.POST.get(f'q-{number}-opt-{option}')
        o = Option(question=q, option=option)
        o.save()
      
      # save the answer data
      answer = request.POST.get(f'q-{number}-answer')
      a = Answer(question=q, answer=answer)
      a.save()
      
    return HttpResponseRedirect(reverse('topic', args=[topic.id, topic.slug]))

  return render(request, "quizApp/make_quiz.html", {
    "Topics": topics,
  })



### API FUNCTIONS


def data_users(request):
    users = User.objects.all()
    return JsonResponse([user.serialize() for user in users], safe=False)

def data_user(request, user_id):
    user = User.objects.get(id=user_id)
    return JsonResponse(user.serialize(), safe=False)

def data_topics(request):
    topics = Topic.objects.all()
    return JsonResponse([topic.serialize() for topic in topics], safe=False)
    
def data_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    return JsonResponse(topic.serialize(), safe=False)
    
def data_quizzes(request):
    quizzes = Quiz.objects.all()
    return JsonResponse([quiz.serialize() for quiz in quizzes], safe=False)
    
def data_quiz(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    return JsonResponse(quiz.serialize(), safe=False)
    
def data_participants(request):
    participants = Participant.objects.all()
    return JsonResponse([participant.serialize() for participant in participants], safe=False)
    
def data_participant(request, participant_id):
    participant = Participant.objects.get(id=participant_id)
    return JsonResponse(participant.serialize(), safe=False)
    