from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from mainApp.models import User
from django.contrib import messages
from reservationsApp.models import Reservation
from loansApp.models import Loan

from reservationsApp.models import Reservation

from loansApp.models import Loan


def login_view(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'usersApp/login.html', context=context)
    if request.method == 'POST':
        pass


# se llama cuando se envia el formulario de login
def login_submit(request):

    username = request.POST['email']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    context = {'error_message': ''}

    if user is not None:
        login(request, user)
        return redirect('/articles/')
    else:
        messages.warning(request, 'La contraseña ingresada no es correcta o el usuario no existe')
        return redirect('/user/login')


# se llama cuando se quiere acceder a la pagina de creacion de cuentas
def signup(request):
    if request.method == 'GET':
        return render(request, 'usersApp/create_account.html')
    if request.method == 'POST':
        pass


# se llama cuando se manda el formulario de creacion de cuentas
def signup_submit(request):

    context = {'error_message': '', }

    if request.method == 'POST':
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        password2 = request.POST['password2']
        rut = request.POST['RUT']

        #Validar que usuario existe
        if User.objects.filter(email = email).exists():
            messages.warning(request, 'Ya existe una cuenta con ese correo.')
            return redirect('/user/signup/')

        #Validar que el formato de Rut sea valido
        elif not rutIsValid(rut):
            messages.warning(request, 'El rut no es valido')
            return redirect('/user/signup/')

        #Validar que rut existe
        elif User.objects.filter(rut = rut).exists():
            messages.warning(request, 'Ya existe una cuenta con ese rut')
            return redirect('/user/signup/')

        #Validar que se haya repetido correctamente la contraseña
        elif (password != password2):
            messages.warning(request, 'Las contraseñas no coinciden')
            return redirect('/user/signup/')
        else:
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password, rut = rut)
            login(request, user)
            messages.success(request, 'Bienvenid@, ' + user.first_name + ' ya puedes comenzar a hacer reservas :)')
            return redirect('/articles/')

def rutIsValid(rut):
    if len(rut) != 10:
        return False
    if rut[8] != '-':
        return False
    try:
        int(rut.split("-")[0])
        if isinstance(rut.split("-")[1], str):
            return True
        return False
    except ValueError:
        return False

@login_required
def logout_view(request):
    logout(request)
    return redirect('/user/login/')


@login_required
def user_data(request, user_id):
    try:
        user = User.objects.get(id=user_id)

        reservations_id = Reservation.objects.values_list('id').filter(user = user_id).order_by('-id')[:10]
        reservations = Reservation.objects.filter(id__in=reservations_id).order_by('-starting_date_time')

        loans_id = Loan.objects.values_list('id').filter(user = user_id).order_by('-id')[:10]
        loans = Loan.objects.filter(id__in=loans_id).order_by('-starting_date_time')

        context = {
            'user': user,
            'reservations': reservations,
            'loans': loans,
        }
        return render(request, 'usersApp/user_profile.html', context)
    except Exception:
        return redirect('/')