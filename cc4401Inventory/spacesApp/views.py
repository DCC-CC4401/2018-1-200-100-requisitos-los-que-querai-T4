from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import models
from datetime import datetime, timedelta
from spacesApp.models import Space
import random, os
import pytz
from django.contrib import messages



@login_required
def ficha_espacio(request, space_id):
    try:
        space = Space.objects.get(id= space_id)
        admin = request.user.is_staff
        context = {'space' : space, 'admin': admin}
        return render(request, 'ficha_espacio.html', context)


    except:
        return redirect('/')