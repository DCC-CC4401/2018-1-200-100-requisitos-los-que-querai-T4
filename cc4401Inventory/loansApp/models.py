from mainApp.models import Action
from articlesApp.models import Article
from django.db import models


class Loan(Action):
    STATES = (
        ('V', 'Vigente'),
        ('R', 'Recibido'),
        ('P', 'Perdido')
    )
    state = models.CharField('Estado', choices=STATES, max_length=1, default='V')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
