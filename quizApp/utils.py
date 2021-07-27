from quizApp.models import Participant
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
import matplotlib as mpl
import numpy as np
import pandas as pd



# grading function
# returns score
# ACTUALLY NOT NEEDED LMAO
def grading(**kwargs):

  """
      function for grading
      questions is a list of queried Question objects ( Quiz.objects.get(id=quiz_id).questions.all() )
      participant_answers is a list of queried Participant => Answer objects ( Participant.objects.get(quiz__id=quiz_id).answers.all() )
  """

  for key, values in kwargs.items():
    if key not in ['request', 'participation_id','questions', 'participant_answers']:
      return "Tidak ada key yang cocok. Masukkan key dengan benar."
    
  request = kwargs['request']
  participation_id = kwargs['participation_id']
  questions = kwargs['questions']
  participant_answers = kwargs['participant_answers']

  grading = []
  number_of_corrects = 0
  number_of_questions = len(questions)
  
  for number in range(0, number_of_questions):

    if questions[number].answer.all()[0].answer == participant_answers[number].answer:
      status = True
      number_of_corrects += 1
    else:
      status = False

    grading.append(
      {
        "number": number+1, # number
        "question": questions[number].question, # the questions
        "real answer": questions[number].answer.all()[0].answer,  # real answers
        "participant answer": participant_answers[number].answer,  # participant answers
        "Correct": status, # Correct/Incorrect
      }
    )
  
  score = float(number_of_corrects / number_of_questions) * 100
  data = Participant.objects.get(id = participation_id)
  data.score = score
  data.save()


  """
    ### THIS BIG-A*S DICTIONARY ISN'T NEEDED ###
  grading_info = [{
    "participation id": participation_id,
    "participant username": request.user.username,
    "number of questions": number_of_questions,
    "number of corrects": number_of_corrects,
    "score": score,
    "details": grading
  }]

  # output example: "media/examples/Example Grading Function Output.png"
  # BEEN CHANGED SINCE THEN I THINK I AM NOT SURE I WON'T BOTHER ANYMORE

  return grading_info
  # return JsonResponse(grading_info, safe=False)

  """
