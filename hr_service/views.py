from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from .models import Candidate, Planet, Jedi, Challenge, Answer

# Create your views here.

def Index(request):
    template = 'hr_service/index.html'
    return render(request, template)

def JediView(request):
    template = 'hr_service/jedi.html'

    jedis = Jedi.objects.all()
    return render(request, template, {'jedis': jedis})

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

        new_candidate = Candidate.objects.create(name=name, planet=planet, age=age, email=email)
    except:
        return render(request, template)
        #return HttpResponse(request, 'hr_service/candidate.html')
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

    answers = []
    for i in Challenge.objects.all():
        if str(i.id) in results:
            answers.append(Answer(result=True, candidate_id=id, question_id=i.id))
        else:
            answers.append(Answer(result=False, candidate_id=id, question_id=i.id))
    
    Answer.objects.bulk_create(answers)
    return render(request, template, {'candidate_name':candidate_name})

def CandidatesView(request, planet_id, jedi_id):
    template = 'hr_service/candidates.html'
    candidates = Candidate.objects.filter(planet_id=planet_id)

    #return HttpResponseRedirect(reverse('candidates:results', args=(planet_id, jedi_id, )))
    return render(request, template, {'candidates':candidates})

def ResultsView(request, planet_id, jedi_id):
    template = 'hr_service/candidate_result.html'

    #return HttpResponseRedirect(reverse('candidates:challenge', args=(planet_id, jedi_id, )))
    return render(request, template)
