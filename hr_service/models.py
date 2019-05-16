from django.db import models

class Planet(models.Model):
    name = models.CharField('Наименование', max_length=50)
    def __str__(self):
        return self.name

class Jedi(models.Model):
    name = models.CharField('Имя', max_length=50)
    planet = models.ForeignKey(Planet, on_delete=models.CASCADE) #'Планета обучения'

class Candidate(models.Model):
    name = models.CharField('Имя', max_length=50)
    planet = models.ForeignKey(Planet, on_delete=models.CASCADE) #'Планета обитания'
    age = models.IntegerField('Возраст', default=0)
    email = models.EmailField('Емейл')

class Challenge(models.Model):
    order = models.IntegerField('Код ордена', unique=True)
    question = models.CharField('Вопрос', max_length=150)

class Answer(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE) #'Кандидат'
    question = models.ForeignKey(Challenge, on_delete=models.CASCADE) #'Вопрос'
    result = models.BooleanField('Ответ', default=False)

class Padawan(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE) #'Кандидат'
    jedi = models.ForeignKey(Jedi, on_delete=models.CASCADE) #'Джедай'
