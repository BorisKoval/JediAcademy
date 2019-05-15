from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from .models import Candidate, Planet, Jedi

# Create your views here.

def Index(request):
    template = 'hr_service/index.html'
    return render(request, template)

def JediView(request):
    template = 'hr_service/jedi.html'

    jedis = Jedi.objects.all()
    return render(request, template, {'jedis': jedis})

def Create(request):
    template = 'hr_service/candidate.html'
    try:
        name = request.POST['name']
        planet = Planet.objects.get(pk=request.POST['planet'])
        age = request.POST['age']
        email = request.POST['email']

        Candidate.objects.create(name=name, planet=planet, age=age, email=email)
    except:
        return render(request, template)
        #return HttpResponse(request, 'hr_service/candidate.html')
    else:
        return HttpResponseRedirect('/challenge')



def CandidateView(request):
    template = 'hr_service/candidate.html'
    planets = Planet.objects.all()

    return render(request, template, {'planets': planets})




def CandidatesView(request, jedi_id):
    template = 'hr_service/candidates.html'

    candidates = Candidate.objets.get(pk=jedi_id)

    return HttpResponseRedirect(reverse('candidates:results', args=(candidates.id,)))




def ChallengeView(request):
    template = 'hr_service/challenge.html'

    return render(request, template)

""" class JediView(generic.ListView):
    template_name = 'hr_service/jedi.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('pub_date')[:5]
 """