from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from .models import Candidate, Planet, Jedi, Challenge, Answer, Padawan, Order
from django.core.mail import send_mail
from django.db.models import Count

def Index(request):
    template = 'hr_service/index.html'
    return render(request, template)

def JediView(request):
    template = 'hr_service/jedi.html'
    jedis_and_padawans = Jedi.objects.annotate(Count('padawan'))
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
        return HttpResponseRedirect(reverse('candidates:challenge', args=(new_candidate.id, new_candidate.planet.id)))

def ChallengeView(request, candidate_id, planet_id):
    template = 'hr_service/challenge.html'

    questions = Challenge.objects.select_related().filter(order__planet_id=planet_id)

    return render(request, template, {'questions':questions,})

def EndChallenge(request, candidate_id, planet_id):
    template = 'hr_service/thanks.html'
    results = request.POST.getlist('answer')

    answers = []
    questions = Challenge.objects.all().select_related().filter(order__planet_id=planet_id)

    #получаем все ответы кандидата и сохраняем
    for question in questions:
        if str(question.id) in results:
            answers.append(Answer(result=True, candidate_id=candidate_id, question_id=question.id))
        else:
            answers.append(Answer(result=False, candidate_id=candidate_id, question_id=question.id))
    
    Answer.objects.bulk_create(answers)
    return render(request, template)

def CandidatesView(request, planet_id, jedi_id): #список кандидатов для Джедая
    template = 'hr_service/candidates.html'

    #фильтрация по планете и проверка является ли кандидат уже падаваном
    candidates = Candidate.objects.select_related().filter(planet_id=planet_id).filter(padawan__isnull=True)

    return render(request, template, {'candidates':candidates, 'jedi_id':jedi_id})

def ResultsView(request, planet_id, jedi_id, candidate_id):
    template = 'hr_service/candidate_result.html'
    
    result_data = Answer.objects.select_related().filter(candidate_id=candidate_id)
    candidate_name = result_data[0].candidate.name

    return render(request, template, {'candidate_name':candidate_name, 'result_data':result_data})

def BecomePadawan(request, planet_id, jedi_id, candidate_id):
    template = 'hr_service/padawan.html'

    #ограничение на кол-во падаванов, не более 3
    if Padawan.objects.filter(jedi_id=jedi_id).count() >= 3:
        return HttpResponseRedirect(reverse('candidates:candidates', args=(planet_id, jedi_id, )))
    
    Padawan.objects.create(candidate_id=candidate_id, jedi_id=jedi_id)
    candidate = Candidate.objects.filter(id=candidate_id)

    send_mail('Поздравляем !', 'Поздравляем, вы зачислены в Падаваны !', 'hr@jediacademy.com',[candidate[0].email])

    return render(request, template, {'candidate':candidate})
