from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from .models import Candidate, Planet, Jedi, Challenge, Answer, Padawan
from django.core.mail import send_mail

# Create your views here.

def Index(request):
    template = 'hr_service/index.html'
    return render(request, template)

def JediView(request):
    template = 'hr_service/jedi.html'
    jedis = Jedi.objects.all()
    
    #добавляем поле "кол-во падаванов"
    jedis_and_padawans = {}
    for jedi in jedis:
        jedis_and_padawans[jedi] = Padawan.objects.filter(jedi_id=jedi.id).count()
    
    return render(request, template, {'jedis_and_padawans': jedis_and_padawans})

def CandidateView(request):
    template = 'hr_service/candidate.html'
    planets = Planet.objects.all()
    return render(request, template, {'planets': planets})

def EnterChallenge(request):
    template = 'hr_service/candidate.html'
    try:
        name = request.POST['name']
        planet = Planet.objects.get(pk=request.POST['planet'])
        age = request.POST['age']
        email = request.POST['email']

        #добавляем нового кандидата в БД
        new_candidate = Candidate.objects.create(name=name, planet=planet, age=age, email=email)
    except:
        return render(request, template)
    else:
        return HttpResponseRedirect(reverse('candidates:challenge', args=(new_candidate.id,)))

def ChallengeView(request, id):
    template = 'hr_service/challenge.html'
    candidate = Candidate.objects.get(pk=id)
    questions = Challenge.objects.all()

    return render(request, template, {'candidate':candidate, 'questions':questions,})

def EndChallenge(request, id):
    template = 'hr_service/thanks.html'
    results = request.POST.getlist('answer')
    candidate_name = Candidate.objects.get(pk=id).name

    answers = [] #получаем все ответы кандидата и сохряняем 
    for i in Challenge.objects.all():
        if str(i.id) in results:
            answers.append(Answer(result=True, candidate_id=id, question_id=i.id))
        else:
            answers.append(Answer(result=False, candidate_id=id, question_id=i.id))
    
    Answer.objects.bulk_create(answers)
    return render(request, template, {'candidate_name':candidate_name})

def CandidatesView(request, planet_id, jedi_id):
    template = 'hr_service/candidates.html'
    #candidates = Candidate.objects.filter(padawan__candidate_id=1, planet_id=planet_id)
    
    candidates = [] #фильтрация по планете и проверка является ли кандидат уже падаваном
    for candidate in Candidate.objects.filter(planet_id=planet_id):
        if Padawan.objects.filter(candidate_id=candidate.id).count() is 0:
            candidates.append(candidate)

    return render(request, template, {'candidates':candidates, 'jedi_id':jedi_id})

def ResultsView(request, planet_id, jedi_id, candidate_id):
    template = 'hr_service/candidate_result.html'
    candidate_name = Candidate.objects.get(pk=candidate_id).name
    answers = Answer.objects.filter(candidate_id=candidate_id)
    
    #создаем словарь "вопрос":"ответ"
    result_data = {}
    for answer in answers:
        result_data[Challenge.objects.get(pk=answer.question_id).question] = answer.result

    return render(request, template, {'candidate_name':candidate_name, 'result_data':result_data})

def BecomePadawan(request, planet_id, jedi_id, candidate_id):
    template = 'hr_service/padawan.html'

    #ограничение на кол-во падаванов
    if Padawan.objects.filter(jedi_id=jedi_id).count() > 3:
        return HttpResponseRedirect(reverse('candidates:candidates', args=(planet_id, jedi_id, )))
    
    Padawan.objects.create(candidate_id=candidate_id, jedi_id=jedi_id)
    candidate = Candidate.objects.get(pk=candidate_id)

    send_mail('Поздравляем !', 'Поздравляем, вы зачислены в Падаваны !', 'hr@jediacademy.com',[candidate.email])

    return render(request, template, {'candidate':candidate})
