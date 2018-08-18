from mainApp.models import Action
from articlesApp.models import Article
from django.db import models


class Loan(Action):
    STATES = (
        ('A', 'Aceptado'),
        ('R', 'Rechazado'),
        ('P', 'Pendiente'),
        ('V', 'Vigente'),
        ('Re', 'Recibido'),
        ('Pe', 'Perdido')
    )
    state = models.CharField('Estado', choices=STATES, max_length=2, default='V')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
