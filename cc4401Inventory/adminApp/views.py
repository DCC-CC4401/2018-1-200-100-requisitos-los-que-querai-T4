from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from reservationsApp.models import Reservation
from loansApp.models import Loan
from articlesApp.models import Article
from spacesApp.models import Space
from mainApp.models import User
from datetime import datetime, timedelta, date
import pytz
from django.utils.timezone import localtime

@login_required
def user_panel(request):
    user = request.user
    if not (user.is_superuser and user.is_staff):
        return redirect('/')
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'user_panel.html', context)

@login_required
def items_panel(request):
    user = request.user
    if not (user.is_superuser and user.is_staff):
        return redirect('/')
    articles = Article.objects.all()
    artistates = Article.STATES
    spaces = Space.objects.all()
    spacestates = Space.STATES
    context = {
        'articles': articles,
        'articlestates': artistates,
        'spaces': spaces,
        'spacestates': spacestates
    }
    return render(request, 'items_panel.html', context)

@login_required
def actions_panel(request):
    user = request.user
    if not (user.is_superuser and user.is_staff):
        return redirect('/')
    try:
        current_week = datetime.strptime(request.GET["date"], "%Y-%m-%d").date().isocalendar()[1]
        current_date = request.GET["date"]
    except:
        current_date = date.today().strftime("%Y-%m-%d")
        current_week = date.today().isocalendar()[1]

    colores = {'A': 'rgba(0,153,0,0.7)',
               'P': 'rgba(51,51,204,0.7)',
               'R': 'rgba(153, 0, 0,0.7)',
               'V': 'rgba(0,153,0,0.7)',
               'Re': 'rgba(0,0,153,0.7)',
               'Pe': 'rgba(153, 0, 0,0.7)'
    }
    reservations = Reservation.objects.filter(state='P').order_by('-pk')
    current_week_reservations = Reservation.objects.filter(starting_date_time__week = current_week)
    actual_date = datetime.now(tz=pytz.utc)
    try:
        if request.method == "GET":
            if request.GET["filter"]=='vigentes':
                loans = Loan.objects.filter(ending_date_time__gt=actual_date, state='V').order_by('starting_date_time')
            elif request.GET["filter"]=='caducados':
                loans = Loan.objects.filter(ending_date_time__lt=actual_date, state='V').order_by('starting_date_time')
            elif request.GET["filter"]=='perdidos':
                loans = Loan.objects.filter(ending_date_time__lt=actual_date, state='Pe').order_by('starting_date_time')
            else:
                loans = Loan.objects.all().order_by('starting_date_time')
    except:
        loans = Loan.objects.all().order_by('-pk')

    res_list = []
    for i in range(5):
        res_list.append(list())
    for r in current_week_reservations:
        reserv = list()
        reserv.append(r.space.name)
        reserv.append(localtime(r.starting_date_time).strftime("%H:%M"))
        reserv.append(localtime(r.ending_date_time).strftime("%H:%M"))
        reserv.append(colores[r.state])
        res_list[r.starting_date_time.isocalendar()[2] - 1].append(reserv)

    move_controls = list()
    move_controls.append(
        (datetime.strptime(current_date, "%Y-%m-%d") + timedelta(weeks=-4)).strftime("%Y-%m-%d"))
    move_controls.append(
        (datetime.strptime(current_date, "%Y-%m-%d") + timedelta(weeks=-1)).strftime("%Y-%m-%d"))
    move_controls.append(
        (datetime.strptime(current_date, "%Y-%m-%d") + timedelta(weeks=1)).strftime("%Y-%m-%d"))
    move_controls.append(
        (datetime.strptime(current_date, "%Y-%m-%d") + timedelta(weeks=4)).strftime("%Y-%m-%d"))

    delta = (datetime.strptime(current_date, "%Y-%m-%d").isocalendar()[2]) - 1
    monday = (
        (datetime.strptime(current_date, "%Y-%m-%d") - timedelta(days=delta)).strftime("%d/%m/%Y"))


    context = {
        'reservations_query': reservations,
        'loans': loans,
        'reservations': res_list,
        'current_date': current_date,
        'controls': move_controls,
        'actual_monday': monday
    }
    return render(request, 'actions_panel.html', context)


def modify_reservations(request):
    user = request.user
    if not (user.is_superuser and user.is_staff):
        return redirect('/')
    if request.method == "POST":

        accept = True if (request.POST["accept"] == "1") else False
        reservations = Reservation.objects.filter(id__in=request.POST.getlist("selected"))
        if accept:
            for reservation in reservations:
                reservation.state = 'A'
                reservation.save()
        else:
            for reservation in reservations:
                reservation.state = 'R'
                reservation.save()

    return redirect('/admin/actions-panel')

def modify_loans(request):
    user = request.user
    if not (user.is_superuser and user.is_staff):
        return redirect('/')
    if request.method == "POST":

        received = True if (request.POST["received"] == "1") \
            else False
        loans = Loan.objects.filter(id__in=request.POST.getlist("selected-loan"))
        if received:
            for loan in loans:
                loan.state = 'Re'
                loan.save()
        else:
            for loan in loans:
                loan.state = 'Pe'
                loan.save()
                loan.article.state = 'L'
                loan.article.save()

    return redirect('/admin/actions-panel')

def create_article(request):
    user = request.user
    if not (user.is_superuser and user.is_staff):
        return redirect('/')
    if request.method == "POST":
        articlename = request.POST['ArticleName']
        articlestate = request.POST['ArticleStateInput']
        articlephoto = request.FILES['ArticlePhoto']
        articledesc = request.POST['ArticleDesc']
        article = Article.objects.create(name= articlename, description= articledesc, image= articlephoto, state=articlestate)
        article.save()

    return redirect('/admin/items-panel')
    #return HttpResponse("crear articulo: " + str(name))

def delete_article(request, article_id):
    articulo= get_object_or_404(Article,pk=article_id)
    articulo.delete()
    return redirect('/admin/items-panel')
