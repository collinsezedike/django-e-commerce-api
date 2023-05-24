from django.urls import path
from . import views

urlpatterns = [
    path("login", views.login, name="user-login"),
    path("logout", views.logout, name="user-logout"),

    path("", views.get_and_create_users, name="user-list-and-create"),
    path("<int:id>", views.read_update_and_delete_user_by_id,
         name="user-detail-update-and-delete"),
]
