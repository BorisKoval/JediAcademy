from django.urls import path
from . import views
from django.urls import include

app_name = 'candidates'
urlpatterns = [
    path('', views.Index, name='index'),
    path('jedi/', views.JediView, name='jedi'),
    path('candidate/', views.CandidateView, name='candidate'),
    path('challenge/', views.EnterChallenge, name='challenge'),
    path(r'<int:candidate_id>/<int:planet_id>/challenge/', views.ChallengeView, name='challenge'),
    path(r'<int:candidate_id>/<int:planet_id>/challenge/thanks/', views.EndChallenge, name='thanks'),
    path(r'jedi/<int:jedi_id>/planet/<int:planet_id>/candidates/', views.CandidatesView, name='candidates'),
    path(r'jedi/<int:jedi_id>/planet/<int:planet_id>/<int:candidate_id>/results/', views.ResultsView, name='results'),
    path(r'jedi/<int:jedi_id>/planet/<int:planet_id>/<int:candidate_id>/results/padawan/', views.BecomePadawan, name='padawan'),
]
