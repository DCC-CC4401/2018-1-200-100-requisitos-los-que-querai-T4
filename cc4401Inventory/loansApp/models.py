from mainApp.models import Action
from articlesApp.models import Article
from spacesApp.models import Space
from django.db import models


class ArticleLoan(Action):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

class SpaceLoan(Action):
    space = models.ForeignKey(Space, on_delete=models.CASCADE)