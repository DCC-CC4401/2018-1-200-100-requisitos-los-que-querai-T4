from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import models
from datetime import datetime, timedelta
from spacesApp.models import Space
import random, os
import pytz
from django.contrib import messages
import datetime
from reservationsApp.models import Reservation
from django.utils.timezone import localtime

@login_required
def ficha_espacio(request, space_id, date=None):

    if date:
        current_date = date
        current_week = datetime.datetime.strptime(current_date,"%Y-%m-%d").date().isocalendar()[1]
    else:
        try:
            current_week = datetime.datetime.strptime(request.GET["date"], "%Y-%m-%d").date().isocalendar()[1]
            current_date = request.GET["date"]
        except:
            current_week = datetime.date.today().isocalendar()[1]
            current_date = datetime.date.today().strftime("%Y-%m-%d")

    reservations = Reservation.objects.filter(starting_date_time__week = current_week, state__in = ['P','A'], id=space_id)
    colores = {'A': 'rgba(0,153,0,0.7)',
               'P': 'rgba(51,51,204,0.7)'}

    res_list = []
    for i in range(5):
        res_list.append(list())
    for r in reservations:
        reserv = []
        reserv.append(r.space.name)
        reserv.append(localtime(r.starting_date_time).strftime("%H:%M"))
        reserv.append(localtime(r.ending_date_time).strftime("%H:%M"))
        reserv.append(colores[r.state])
        res_list[r.starting_date_time.isocalendar()[2]-1].append(reserv)

    move_controls = list()
    move_controls.append((datetime.datetime.strptime(current_date,"%Y-%m-%d")+datetime.timedelta(weeks=-4)).strftime("%Y-%m-%d"))
    move_controls.append((datetime.datetime.strptime(current_date,"%Y-%m-%d")+datetime.timedelta(weeks=-1)).strftime("%Y-%m-%d"))
    move_controls.append((datetime.datetime.strptime(current_date,"%Y-%m-%d")+datetime.timedelta(weeks=1)).strftime("%Y-%m-%d"))
    move_controls.append((datetime.datetime.strptime(current_date,"%Y-%m-%d")+datetime.timedelta(weeks=4)).strftime("%Y-%m-%d"))

    delta = (datetime.datetime.strptime(current_date, "%Y-%m-%d").isocalendar()[2])-1
    monday = ((datetime.datetime.strptime(current_date, "%Y-%m-%d") - datetime.timedelta(days=delta)).strftime("%d/%m/%Y"))

    try:
        space = Space.objects.get(id= space_id)
        if request.user.is_staff:
            admin = 1
        else:
            admin = 0
        context = {'space' : space, 'admin': admin}
        admin = request.user.is_staff
        context = {'space' : space,
                   'reservations' : res_list,
                   'current_date' : current_date,
                   'controls' : move_controls,
                   'actual_monday' : monday,
                   'admin': admin}
        return render(request, 'ficha_espacio.html', context)


    except:
        return redirect('/')

@login_required
def update_space(request):
    if request.method == 'POST':
        id = request.POST['id']
        space = Space.objects.get(pk=id)
        space.name = request.POST['name']
        space.capacidad = request.POST['capacidad']
        space.description = request.POST['description']
        space.state = request.POST['status']
        space.save()
        print("HOLAA")
        return redirect('/space/' + id)
    else:
        return HttpResponse("Whoops!")