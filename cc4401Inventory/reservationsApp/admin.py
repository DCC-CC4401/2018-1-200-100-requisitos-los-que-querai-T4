from django.contrib import admin
from .models import ArticleReservation
from .models import SpaceReservation

# Register your models here.
admin.site.register(ArticleReservation)
admin.site.register(SpaceReservation)