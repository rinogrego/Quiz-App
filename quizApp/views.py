from random import shuffle
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

from .models import User, Quiz, Question, Topic, Participant, ParticipantAnswer
import json
from random import shuffle
from .utils import grading
from datetime import datetime



def index(request):

  topics = Topic.objects.all()
  contributors = [user for user in User.objects.all() if user.has_contribution()]
  return render(request, "quizApp/index.html", {
    "Topics": topics,
    "Contributors": contributors,
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


def profile(request, username):
  user = User.objects.get(username=username)
  my_quizzes = Quiz.objects.filter(creator__username=username)
  return render(request, "quizApp/profile.html", {
    "User": user,
    "myQuizzes": my_quizzes,
  })


def study(request):
  topics = Topic.objects.all()
  return render(request, "quizApp/study.html", {
    "Topics": topics
  })


def topic(request, topic_id, topic_slug):
  quizzes = Quiz.objects.filter(topic__id=topic_id, topic__slug=topic_slug)
  return render(request, "quizApp/topic.html", {
    "Quizzes": quizzes
  })


def test(request, quiz_id, quiz_slug):

  quiz = Quiz.objects.get(id=quiz_id, slug=quiz_slug)
  questions = quiz.questions.all()

  # pagination
  # paginator = Paginator(questions, 1)
  # page_number = request.GET.get('page', 1)
  # page_obj = paginator.get_page(page_number) # this is a list even though only 1 question object queried

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

  return render(request, "quizApp/test.html", {
    "Quiz": quiz,
    # "Questions": page_obj,
    "Questions": questions,
    "Questions_Length": questions_for_nav,
  })


def answers(request, quiz_id, quiz_slug):

  participant = Participant.objects.get(user=request.user, quiz__id=quiz_id)
  quiz = Quiz.objects.get(id=quiz_id)
  questions = quiz.questions.all()

  # grading(request=request, participation_id = participant.id, questions=questions, participant_answers=participant.answers.all() )
  # results returns a list containing json objects of information
  # output example: "media/examples/Example Grading Function Output.png"
  # IN THE END, THAT WASN"T NEEDED LOL

  questions_length = [number for number in range(1, len(questions)+1)]

  questions_for_nav = {}
  for number in questions_length:
    questions_for_nav[number] = ""
  for number in  range(0, len(questions)):
    questions_for_nav[number+1] = questions[number].id
  # questions_for_nav = {number of a question: question.id}
  
  if request.method == "POST":

    # save the finished date
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


  # grading score ( I feel there is a better way to do this )
  grading(request=request, participation_id = participant.id, questions=questions, participant_answers=participant.answers.all() )
  # RE-Query ParticipantAnswer after the answers has been saved and answers has been graded (scored).
  participant = Participant.objects.get(user=request.user, quiz__id=quiz_id)

  
  return render(request, "quizApp/answers.html", {
    "Participant": participant,
    "Quiz": quiz,
    "Questions": questions,
    "Questions_Length": questions_for_nav,
  })


def make_quiz(request):
  if request.method == "POST":
    # do something
    pass
  return render(request, "quizApp/make_quiz.html")


# this one may be omitted because my_quiz may be a one page with profile
def my_quiz(request, user_id):
  return True











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
    