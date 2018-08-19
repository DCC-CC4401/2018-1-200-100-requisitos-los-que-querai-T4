from django.urls import path
from . import views

urlpatterns = [
    path('delete/', views.delete, name='delete_reservation'),
    path('<int:reservation_id>', views.reservation_data, name='reservation_data'),
    path('<int:reservation_id>/cancel_reservation', views.cancel_reservation, name='cancel_reservation')
]
