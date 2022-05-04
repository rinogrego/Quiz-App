from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Avg

# Create your models here.

class User(AbstractUser):
  
  image = models.ImageField(upload_to='media/profile/', default='media/profile/user.png')
  date = models.DateTimeField(auto_now_add=True)
  year = models.IntegerField(null=True, blank=False)
  follows = models.ManyToManyField("self", related_name="followers", symmetrical=False, blank=True)
  LEVEL_CHOICES = (
    ('O', 'Other'),
    ('C', 'College Students'),
    ('G', 'Graduate'),
    ('W', 'Working'),
  )
  level = models.CharField(max_length=50, choices=LEVEL_CHOICES, default='Other')

  def has_contribution(self):
    if self.quizzes.count() > 0:
      return True
    else:
      return False

  def has_participated(self):
    if self.quizzes_taken.count() > 0:
      return True
    else:
      return False

  def status(self):
    if self.has_participated() == True and self.has_contribution() == True:
      return "Learner / Contributor"
    elif self.has_participated() == True:
      return "Learner"
    elif self.has_contribution() == True:
      return "Contributor"
    else:
      return "Sightseeing"

  def date_mm_dd_yy(self):
    return str(self.date.strftime("%b %d, %Y"))

  def contribution_count(self):
    return self.quizzes.count()

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

  def quiz_count(self):
    return Quiz.objects.filter(topic=self.id).count()

  def contributors(self):
    # query Users dimana quizzes yang mereka miliki ada di query set: quiz-quiz yang memiliki topic sesuai id topic (????? This works?)
    contributors = User.objects.filter(quizzes__in=Quiz.objects.filter(topic=self.id)).all()
    return [contributor.username for contributor in contributors]

  def participant(self):
    # return Participant.objects.filter(quiz__in=Quiz.objects.filter(topic=self)).count()
    participants = Participant.objects.filter(quiz__in=Quiz.objects.filter(topic=self)).all()
    # output: participants is still a list where each element's user isn't unique with each other
    # in other words, a user that has attempted a same quiz x times will be counted as x participant even though the user/participant is just one.
    unique_participants = []
    try:
      for participant in participants:
        if participant.user.id not in [participant.user.id for participant in unique_participants]:
          unique_participants.append(participant)
    except:
      pass

    return len(unique_participants)

    
  def __str__(self):
    return self.title


class Quiz(models.Model):
  slug = models.SlugField(max_length=40, null=True)
  title = models.CharField(max_length=40, null=False, blank=False, default="Untitled")
  creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quizzes")
  topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="quizzes")
  date = models.DateTimeField(auto_now_add=True)
  # passing_grade = models.IntegerField()

  def average_score(self):
    result = Participant.objects.filter(quiz__id=self.id).aggregate(Avg("score"))
    return result["score__avg"]
  
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
    return f"{self.question}"
    
  def participant_is_correct(self):
    # return ParticipantAnswer.objects.get(question=self.id).answer == Answer.objects.get(question=self.id).answer #returns a single record. WORKS IF only one attempt allowed
    return ParticipantAnswer.objects.filter(question=self.id).order_by('-id')[0].answer == Answer.objects.filter(question=self.id).order_by('-id')[0].answer # get THE LATEST ATTEMPT data
    # return str(self.answer.all()[0]) == str(self.participant_answer.get(participant_id=self.number).answer)

  # hackery, sorry.
  # this is just so that I can pass a variable from views.py to models.py
  # this thing may be really dynamic
  number = models.IntegerField(null=True)
  def what_participant_answer(self):
    # return str(self.participant_answer.get(participant__id=16).answer)
    # return ParticipantAnswer.objects.get(question=self.id).answer #returns a single record. WORKS IF only one attempt allowed
    return ParticipantAnswer.objects.filter(question=self.id).order_by('-id')[0].answer # get THE LATEST ATTEMPT data
    # return str(self.participant_answer.get(participant_id=self.number).answer) <== FUTURE Note : This is wrong
    # FUTURE Note
    # return str(self.particiapnt_answer.get(quiz__id=quiz.id).answer); should have quiz = models.ForeignKey in ParticipantAnswer model.

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
  time_start = models.DateTimeField()
  time_finished = models.DateTimeField()
  score = models.IntegerField()

  def average(self):
    return self.objects.all()

  def time_spent(self):
    try:
      day_hours = str(self.time_finished - self.time_start).split(".")[0]
      try:
        day = day_hours.split(", ")[0]
        hours = day_hours.split(", ")[1].split(':')[0]
        minutes = day_hours.split(", ")[1].split(':')[1]
        seconds = day_hours.split(", ")[1].split(':')[2]
        return f'{day}, {hours} Hours, {minutes} Minutes, {seconds} Seconds'
      except:
        hours = day_hours.split(':')[0]
        minutes = day_hours.split(':')[1]
        seconds = day_hours.split(':')[2]
        if int(hours) == 0:
          return f'{minutes} Minutes, {seconds} Seconds'
        return f"{hours} Hours, {minutes} Minutes, {seconds} Seconds"
    except:
      return self.time_finished

  def serialize(self):
    return {
      "id": self.id,
      "user": self.user.username,
      "quiz": self.quiz.title,
      "time_start": self.time_start.strftime("%b-%d %Y, %I:%M %p"),
      "time_finished": self.time_finished.strftime("%b-%d %Y, %I:%M %p"),
      "score": self.score,
    }

  def __str__(self):
    return F"{self.user.username} for quiz: {self.quiz.title} by {self.quiz.creator.username}"


class ParticipantAnswer(models.Model):
  participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="answers")
  question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="participant_answer")
  answer = models.CharField(max_length=200, null=False, blank=False, default="")

  def is_correct(self):
    return ( self.answer == self.question.answer )

  def __str__(self):
      return self.answer


class ErrorMessage(models.Model):
  message = models.CharField(max_length=500, null=True, blank=True)
  email = models.EmailField()

  def __str__(self):
    return f'{self.email} said: "{self.message}"'