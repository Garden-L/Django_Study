from django.shortcuts import render
from .models import Question
# Create your views here.

def index(request):
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list' : question_list}
    #print(context)
    return render(request, 'pybo/question_list.html', context)