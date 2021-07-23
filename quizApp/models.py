from typing import AbstractSet
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.expressions import Random
from django.db.models.fields import related
from django.db.models import Avg

# Create your models here.

class User(AbstractUser):
  
  # major/status = models.CharField(max_length=30, null=False, blank=False) # multiple choice : college student, high school student, working
  # picture
  year = models.IntegerField(null=True, blank=False)
  follows = models.ManyToManyField("self", related_name="followers", symmetrical=False, blank=True)

  def has_contribution(self):
    if self.quizzes.count() > 0:
      return True
    else:
      return False
  
  def serialize(self):
    return {
      "id": self.id,
      "username": self.username,
      "email": self.email,
      # "major": self.major,
      "year": self.year,
      "number_of_following": self.follows.count(),
      "following": [account_followed.username for account_followed in self.follows.all()],
      "number_of_followers": self.followers.count(),
      "followers": [follower.username for follower in self.followers.all()],
      "quizzes_created": self.quizzes.count(),
      "quizzes_created_detail": [{
        "id": quiz.id,
        "title": quiz.title,
        "topic": quiz.topic.title,
        "date": quiz.date.strftime("%b-%d %Y, %I:%M %p"),
        "number_of_questions": quiz.questions.count()
      } for quiz in self.quizzes.all()],
      "quizzes_taken": self.quizzes_taken.count(),
      "quizzes_taken_detail": [{
        "id": quiz_taken.id,
        "quiz": quiz_taken.quiz.title,
        "score": quiz_taken.score,
      } for quiz_taken in self.quizzes_taken.all()],
    }
  


class Topic(models.Model):
  slug = models.SlugField(max_length=40, default="other")
  title = models.CharField(max_length=40, null=False, blank=False, default="Other")

  def serialize(self):
    return {
      "id": self.id,
      "title": self.title,
      "total": self.quizzes.count(),
      "quizzes": [{
        "title": quiz.title,
        "creator": quiz.creator.username,
        } for quiz in self.quizzes.all()],
    }
    
  def __str__(self):
    return self.title


class Quiz(models.Model):
  slug = models.SlugField(max_length=40, null=True)
  title = models.CharField(max_length=40, null=False, blank=False, default="Untitled")
  creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quizzes")
  topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="quizzes")
  date = models.DateTimeField(auto_now_add=True)
  # passing_grade = models.IntegerField()
  
  def serialize(self):
    return {
      "id": self.id,
      "title": self.title,
      "creator": self.creator.username,
      "topic": self.topic.title,
      "date": self.date.strftime("%b-%d %Y, %I:%M %p"),
      "questions_total": self.questions.count(),
      "questions": [{
        "question": question.question,
        # "options": ,
        # "answer": ,
      } for question in self.questions.all()],
    }

  def __str__(self):
      return self.title


class Question(models.Model):
  quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
  question = models.CharField(max_length=500)

  def serialize(self):
    return {
      "id": self.id,
      "quiz": self.quiz.title,
      "question": self.question,
      "option": [option.option for option in self.options.all()],
      "answer": self.answer.answer,
    }

  def __str__(self):
    return f"{self.id}:  {self.question}"

  def participant_is_correct(self):
    return str(self.answer.all()[0]) == str(self.participant_answer.all()[0])

  def what_participant_answer(self):
    return str(self.participant_answer.all()[0])

  def real_answer(self):
    return str(self.answer.all()[0])


class Option(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
  option = models.CharField(max_length=200, null=True, blank=True)

  def __str__(self):
    return f"option: {self.option}"

  def str_option(self):
    return str(self.option)


class Answer(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answer")
  answer = models.CharField(max_length=200, null=True, blank=True)
  
  def __str__(self):
    return self.answer


class Participant(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quizzes_taken")
  quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="taken_by")
  time_start = models.DateTimeField(auto_now_add=True)
  time_finished = models.DateTimeField()
  score = models.IntegerField()

  def average(self):
    return self.aggregate(Avg('score'))

  def time_spent(self):
    return str(self.time_finished - self.time_start).split(".")[0]

  def serialize(self):
    return {
      "id": self.id,
      "user": self.user.username,
      "quiz": self.quiz.title,
      "time_start": self.time_start.strftime("%b-%d %Y, %I:%M %p"),
      "time_finished": self.time_finished.strftime("%b-%d %Y, %I:%M %p"),
      "score": self.score,
    }


class ParticipantAnswer(models.Model):
  participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="answers")
  question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="participant_answer")
  answer = models.CharField(max_length=200, null=False, blank=False, default="")

  def is_correct(self):
    return ( self.answer == self.question.answer )

  def __str__(self):
      return self.answer