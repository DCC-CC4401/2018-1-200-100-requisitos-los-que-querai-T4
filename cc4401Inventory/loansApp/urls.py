from django.urls import path

from . import views

urlpatterns = [
    path('<int:loan_id>', views.loan_data, name='loan_data'),
    path('<int:loan_id>/lost_request', views.lost_request, name='lost_request'),
    path('<int:loan_id>/cancel_request', views.cancel_request, name='cancel_request')
]