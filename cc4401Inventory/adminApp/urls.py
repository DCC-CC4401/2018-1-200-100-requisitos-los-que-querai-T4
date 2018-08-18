from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_panel, name="landing-panel"),
    path('user-panel/', views.user_panel, name="user-panel"),
    path('items-panel/', views.items_panel, name="items-panel"),
    path('actions-panel/', views.actions_panel, name="actions-panel"),
    path('actions-panel/modifyreservs', views.modify_reservations, name="modify_reservations"),
    path('actions-panel/modifyloans', views.modify_loans, name="modify_loans"),
    path('items-panel/create-article', views.create_article, name="create_article"),
    path('items-panel/delete-article/<int:article_id>', views.delete_article, name="delete_article")
]
