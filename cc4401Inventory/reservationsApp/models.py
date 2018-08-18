from mainApp.models import Action
from spacesApp.models import Space
from django.db import models


class Reservation(Action):
    STATES = (
        ('A', 'Aceptado'),
        ('R', 'Rechazado'),
        ('P', 'Pendiente'),
        ('V', 'Vigente'),
        ('Re', 'Recibido'),
        ('Pe', 'Perdido')
    )
    state = models.CharField('Estado', choices=STATES, max_length=2, default='P')
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
