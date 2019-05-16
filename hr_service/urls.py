from django.urls import path
from . import views
from django.urls import include

app_name = 'candidates'
urlpatterns = [
    path('', views.Index, name='index'),
    path('jedi/', views.JediView, name='jedi'),
    path('candidate/', views.CandidateView, name='candidate'),
    path('challenge/', views.EnterChallenge, name='challenge'),
    path(r'<int:id>/challenge/', views.ChallengeView, name='challenge'),
    path(r'<int:id>/challenge/thanks/', views.EndChallenge, name='thanks'),
    path(r'<int:jedi_id>/<int:planet_id>/candidates/', views.CandidatesView, name='candidates'),
    path(r'<int:jedi_id>/<int:planet_id>/results/', views.ResultsView, name='results'),

    #path('create/', views.Create, name='create'),
    #path('<int:candidate_id>/candidate/', views.CandidatesView, name='candidates'),
]
