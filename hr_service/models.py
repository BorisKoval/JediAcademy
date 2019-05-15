from django.db import models

# Create your models here.
class Planet(models.Model):
    name = models.CharField('Наименование', max_length=50)
    def __str__(self):
        return self.name

class Candidate(models.Model):
    name = models.CharField('Имя', max_length=50)
    planet = models.ForeignKey(Planet, on_delete=models.CASCADE) #'Планета обитания'
    age = models.IntegerField('Возраст', default=0)
    email = models.EmailField('Емейл')
    is_padawan = models.BooleanField('Является падаваном', default=False)

class Jedi(models.Model):
    name = models.CharField('Имя', max_length=50)
    planet = models.ForeignKey(Planet, on_delete=models.CASCADE) #'Планета обучения'
    padawan_count = models.IntegerField('Кол-во падаванов', default=0)

class Challenge(models.Model):
    order = models.IntegerField('Код ордена', unique=True)
    question = models.CharField('Вопрос', max_length=150)

class Answer(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE) #'Кандидат'
    question = models.ForeignKey(Challenge, on_delete=models.CASCADE) #'Вопрос'
    result = models.BooleanField('Ответ', default=False)
