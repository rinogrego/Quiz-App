from django.contrib import admin

# Register your models here.
from .models import User, Topic, Quiz, Question, Option, Answer, Participant, ParticipantAnswer




class UserAdmin(admin.ModelAdmin):
  filter_horizontal = ("follows", )
  list_display = ("id", "username","year")


# Topic --> Quizzes
class TopicAdmin(admin.ModelAdmin):
  list_display = ("id", "title")


# Quiz --> Questions -> Options
#     |              -> Answer
#     |
#     |--> Questions -> Options
#                    -> Answer
class OptionAdmin(admin.ModelAdmin):
  list_display = ("id", "question", "option")

class OptionInline(admin.TabularInline):
  model = Option

class AnswerAdmin(admin.ModelAdmin):
  list_display = ("id", "question", "answer")

class AnswerInline(admin.TabularInline):
  model = Answer

class QuestionAdmin(admin.ModelAdmin):
  # things to be shown OUTSIDE
  list_display = ("id", "quiz", "question")
  # things to be shown INSIDE
  fields = ['quiz', 'question']
  inlines = [
    OptionInline,
    AnswerInline
  ]

class QuestionInline(admin.TabularInline):
  model = Question

class QuizAdmin(admin.ModelAdmin):
  list_display = ("id", "title", "creator", "topic", "date")
  # for showing One-To-Many Relationship
  inlines = [
    QuestionInline
  ]


# Participant
class ParticipantAnswerAdmin(admin.ModelAdmin):
  list_display = ("id", "participant", "answer")

class ParticipantAnswerInline(admin.TabularInline):
  model = ParticipantAnswer

class ParticipantAdmin(admin.ModelAdmin):
  list_display = ("id" ,"user", "quiz", "score", "time_start", "time_finished")
  inlines = [
    ParticipantAnswerInline
  ]



admin.site.register(User, UserAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(ParticipantAnswer, ParticipantAnswerAdmin)

