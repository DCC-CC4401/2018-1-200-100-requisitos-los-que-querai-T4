from django.contrib import admin
from .models import ArticleLoan
from .models import SpaceLoan
# Register your models here.

admin.site.register(ArticleLoan)
admin.site.register(SpaceLoan)