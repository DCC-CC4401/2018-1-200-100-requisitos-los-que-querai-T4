from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_panel, name="landing-panel"),
    path('user-panel/', views.user_panel, name="user-panel"),
    path('items-panel/', views.items_panel, name="items-panel"),
    path('actions-panel/', views.actions_panel, name="actions-panel"),
    path('actions-panel/modify', views.modify_reservations, name="modify_reservations"),
    path('items-panel/create-article', views.create_article, name="create_article")

]
