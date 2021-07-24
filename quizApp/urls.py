from django.urls import path
from . import views

urlpatterns = [
  path("", views.index, name="index"),
  path("login", views.login_view, name="login"),
  path("logout", views.logout_view, name="logout"),
  path("register", views.register, name="register"),
  path("profile/<str:username>", views.profile, name="profile"),
  path("profile/<str:username>/create-quiz", views.make_quiz, name="make_quiz"),
  path("study", views.study, name="study"),
  path("study/<int:topic_id>/<str:topic_slug>", views.topic, name="topic"),
  path("test/<int:quiz_id>/<str:quiz_slug>", views.test, name="test"),
  path("test/<int:quiz_id>/<str:quiz_slug>/<int:participant_id>/answers", views.answers, name="answer"),

  # API Route
  path("data/users", views.data_users, name="data_users"),
  path("data/users/<int:user_id>", views.data_user, name="data_user"),
  path("data/topics", views.data_topics, name="data_topics"),
  path("data/topics/<int:topic_id>", views.data_topic, name="data_topic"),
  path("data/quizzes", views.data_quizzes, name="data_quizzes"),
  path("data/quizzes/<int:quiz_id>", views.data_quiz, name="data_quiz"),
  path("data/participants", views.data_participants, name="data_participants"),
  path("data/participants/<int:participant_id>", views.data_participant, name="data_participant"),
]