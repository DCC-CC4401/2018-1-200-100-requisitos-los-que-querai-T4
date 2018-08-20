from django.shortcuts import render, redirect
from .models import Reservation
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def delete(request):
    if request.method == 'POST':
        reservation_ids = request.POST.getlist('reservation')
        try:
            for reservation_id in reservation_ids:
                reservation = Reservation.objects.get(id=reservation_id)
                if reservation.state == 'P':
                    reservation.delete()
        except:
            messages.warning(request, 'Ha ocurrido un error y la reserva no se ha eliminado')

        return redirect('user_data', user_id=request.user.id)


@login_required
def reservation_data(request, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id)
        user = request.user

        context = {
            'reservation': reservation,
            'user': user
        }

        return render(request, 'reservation_data.html', context)

    except Exception as e:
        print(e)
        return redirect('/')

@login_required
def cancel_reservation(request, reservation_id):
    if request.method == 'POST':
        reservation = Reservation.objects.get(id=reservation_id)
        reservation.delete()
        return redirect('landing_spaces')