from django.urls import path
from . import views
from django.urls import include

app_name = 'candidates'
urlpatterns = [
    path('', views.Index, name='index'),
    path('jedi/', views.JediView, name='jedi'),
    path('candidate/', views.CandidateView, name='candidate'),
    path('create/', views.Create, name='create'),
    path('challenge/', views.ChallengeView, name='challenge'),
    path('candidates/', views.CandidatesView, name='candidates'),
    path('<int:candidate_id>/candidate/', views.CandidatesView, name='candidates'),
]
