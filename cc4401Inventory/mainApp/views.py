from django.shortcuts import render, redirect
from django.utils.timezone import localtime
import datetime
from articlesApp.models import Article
from reservationsApp.models import Reservation
from spacesApp.models import Space
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


@login_required
def landing_articles(request):
    productos = Article.objects.all()
    context = {
        'productos' : productos
    }
    return render(request, 'articulos.html', context)


@login_required
def landing_spaces(request, date=None):

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

    #reservations = Reservation.objects.filter(starting_date_time__week = current_week, state__in = ['P','A'])
    #colores = {'A': 'rgba(0,153,0,0.7)',
    #           'P': 'rgba(51,51,204,0.7)'}

    reservations = Reservation.objects.filter(starting_date_time__week=current_week, state__in=['A', 'V'])
    colores = {'A': 'rgba(0,153,0,0.7)',
               'V': 'rgba(153, 0, 204,0.7)'}
    res_list = []
    for i in range(5):
        res_list.append(list())
    for r in reservations:
        reserv = []
        reserv_state = r.state
        str_state = ""
        if(reserv_state == 'A'):
            str_state = "Aceptado"
        if(reserv_state == 'P'):
            str_state = "Pendiente"
        space_name = r.space.name + " - " + str_state
        #reserv.append(r.space.name)
        reserv.append(space_name)
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

    allSpaces = Space.objects.all()
    spaceOptions = []
    for space in allSpaces:
        spaceOptions.append(space.name)

    fechaMin = (datetime.datetime.strptime(current_date,"%Y-%m-%d")+datetime.timedelta(hours=1)).strftime("%Y-%m-%d")


    context = {'reservations' : res_list,
               'current_date' : current_date,
               'controls' : move_controls,
               'actual_monday' : monday,
               'spaceOptions' : spaceOptions,
               'fechaMin' : fechaMin}
    return render(request, 'espacios.html', context)

@login_required
def landing_spaces_modal(request, modalActivado, spaces, ini_t, fin_t, date=None):

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

    reservations = Reservation.objects.filter(starting_date_time__week=current_week, state__in=['A', 'V'])
    colores = {'A': 'rgba(0,153,0,0.7)',
               'V': 'rgba(153, 0, 204,0.7)'}

    res_list = []
    for i in range(5):
        res_list.append(list())
    for r in reservations:
        reserv = []
        reserv_state = r.state
        str_state = ""
        if (reserv_state == 'A'):
            str_state = "Aceptado"
        if (reserv_state == 'P'):
            str_state = "Pendiente"
        space_name = r.space.name + " - " + str_state
        # reserv.append(r.space.name)
        reserv.append(space_name)
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

    """allSpaces = Space.objects.all()
    spaceOptions = []
    for space in allSpaces:
        spaceOptions.append(space.name)"""

    #fechaMin = (datetime.datetime.strptime(current_date,"%Y-%m-%d")+datetime.timedelta(hours=1)).strftime("%Y-%m-%d")


    context = {'reservations' : res_list,
               'current_date' : current_date,
               'controls' : move_controls,
               'actual_monday' : monday,
               'spaceOptions' : spaces,
               'modalState': 1,
               'modal' : modalActivado,
               'initial_datetime' : ini_t,
               'final_datetime' : fin_t}
    return render(request, 'espacios.html', context)

@login_required
def landing_search(request, products):
    if not products:
        return landing_articles(request)
    else:
        context = {'productos' : products,
                   'colores' : {'D': '#009900',
                                'R': '#ffcc00',
                                'P': '#3333cc',
                                'L': '#cc0000'}
                   }
        return render(request, 'articulos.html', context)


@login_required
def search(request):
    if request.method == "GET":
        query = request.GET['query']
        #a_type = "comportamiento_no_definido"
        a_state = "A" if (request.GET['estado'] == "A") else request.GET['estado']

        if not (a_state == "A"):
            articles = Article.objects.filter(state=a_state,name__icontains=query.lower())
        else:
            articles = Article.objects.filter(name__icontains=query.lower())

        products = None if (request.GET['query'] == "") else articles
        return landing_search(request, products)

def formatFecha(dt):
    #'2018-08-18T09:00'
    res = ''
    res+= str(dt.year) + '-' + str(dt.month) + '-' + str(dt.day) + 'T' + str(dt.hour) + ':'+ str(dt.minute)
    return res

def reservaEspacio(request):
    if request.method == "POST":
        semana = request.POST["semana"]

        initial_t = request.POST["hiddenini"]
        datetime_inicial = semana + "T" + initial_t
        datetime_object2 = datetime.datetime.strptime(datetime_inicial, '%Y-%m-%dT%H:%M')

        final_t = request.POST["hiddenfin"]
        datetime_final = semana + "T" + final_t
        final_datetime = datetime.datetime.strptime(datetime_final, '%Y-%m-%dT%H:%M')

        day = request.POST["hiddendia"]

        if day == "Martes":
            datetime_object2 = datetime_object2 + datetime.timedelta(days=1)
            final_datetime = final_datetime + datetime.timedelta(days=1)
        elif day == "Miercoles":
            datetime_object2 = datetime_object2 + datetime.timedelta(days=2)
            final_datetime = final_datetime + datetime.timedelta(days=2)
        elif day == "Jueves":
            datetime_object2 = datetime_object2 + datetime.timedelta(days=3)
            final_datetime = final_datetime + datetime.timedelta(days=3)
        elif day == "Viernes":
            datetime_object2 = datetime_object2 + datetime.timedelta(days=4)
            final_datetime = final_datetime + datetime.timedelta(days=4)

        """return HttpResponse(datetime_object2)
        initial_t = request.POST["hiddenini"]
        final_t = request.POST["hiddenfin"]
        day = request.POST["hiddendia"]
        if day=="Lunes":
            fecha = day + initial_t + final_t
        return HttpResponse(fecha)
        initial_t = request.POST['t_inicio']
        final_t = request.POST['t_final']
        datetime_object2 = datetime.datetime.strptime(initial_t, '%Y-%m-%dT%H:%M')
        """
        datetime_object3 = datetime_object2-datetime.timedelta(hours=1)
        datetime_object4 = datetime_object2-datetime.timedelta(hours=24)

        #initial_datetime = datetime_object2 +  datetime.timedelta(hours=3)
        #final_datetime = datetime.datetime.strptime(final_datetime, '%Y-%m-%dT%H:%M')
        #final_datetime = final_datetime + datetime.timedelta(hours=3)

        if(datetime_object3 < datetime.datetime.now()):
            listaEspacios = []
            return landing_spaces_modal(request, "#myModal1",listaEspacios, 0, 0)
        if (datetime_object4 < datetime.datetime.now()):
            listaEspacios = Space.objects.exclude(name="Quincho")

            reservas = (Reservation.objects.filter(starting_date_time__range=[initial_datetime, final_datetime]) | \
                        Reservation.objects.filter(ending_date_time__range=[initial_datetime, final_datetime])) & \
                         Reservation.objects.filter(state='A')

            for reserva in reservas:
                id_object = reserva.id
                space = Space.objects.get(id=id_object)
                if space in listaEspacios:
                    listaEspacios = listaEspacios.exclude(id=id_object)

            #spaces = Space.objects.exclude(name = "Quincho")
            return landing_spaces_modal(request, "#myModal2", listaEspacios, formatFecha(initial_datetime), formatFecha(final_datetime))
        else:
            listaEspacios = Space.objects.all()

            reservas = (Reservation.objects.filter(starting_date_time__range=[initial_datetime, final_datetime]) | \
                        Reservation.objects.filter(ending_date_time__range=[initial_datetime, final_datetime])) & \
                         Reservation.objects.filter(state='A')

            for reserva in reservas:
                id_object = reserva.id
                space = Space.objects.get(id=id_object)
                if space in listaEspacios:
                    listaEspacios = listaEspacios.exclude(id=id_object)

            #spaces = Space.objects.exclude(name = "Quincho")
            return landing_spaces_modal(request, "#myModal2", listaEspacios, formatFecha(initial_datetime), formatFecha(final_datetime))
    else:
        return redirect("/")

def crearReserva(request):
    if request.method == "POST":
        espacio = request.POST['espacio']
        id_espacio = int(espacio)
        espacioSel = Space.objects.get(id=id_espacio)

        initial_datetime = request.POST['ini_time']
        datetime_object2 = datetime.datetime.strptime(initial_datetime, '%Y-%m-%dT%H:%M')

        final_datetime = request.POST['fin_time']
        datetime_object3 = datetime.datetime.strptime(final_datetime, '%Y-%m-%dT%H:%M')

        #b = Blog(name='Beatles Blog', tagline='All the latest Beatles news.')
        r = Reservation(space=espacioSel, starting_date_time=datetime_object2, ending_date_time=datetime_object3, state='P', user=request.user)
        r.save()
        return landing_spaces(request)
    else:
        return redirect("/")


"""
 if (fecha_inicio != "") & (fecha_fin != ""):
                    reservas = Reserva.objects.filter(estado_reserva="Aceptada") & \
                               (Reserva.objects.filter(fh_ini_reserva__range=[fecha_inicio, fecha_fin]) | \
                                Reserva.objects.filter(fh_fin_reserva__range=[fecha_inicio, fecha_fin]))

                    for reserva in reservas:
                        id_object = reserva.object_id
                        object = Articulo.objects.get(id=id_object)
                        if object in lista:
                            lista = lista.exclude(id=id_object)"""
