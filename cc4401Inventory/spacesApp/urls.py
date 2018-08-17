from django.urls import path

from . import views

urlpatterns = [
    path('<int:space_id>', views.ficha_espacio, name='ficha_espacio'),
]
