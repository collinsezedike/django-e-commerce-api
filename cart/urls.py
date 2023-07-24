from django.urls import path

from . import views

urlpatterns = [
    path("", views.read_cart, name="cart-item-list"),
    path("add/", views.add_to_cart, name="add-cart-item"),
    path("remove/", views.remove_from_cart, name="remove-cart-item"),
]