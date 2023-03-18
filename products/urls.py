from django.urls import path
from . import views

urlpatterns = [
    path("", views.read_and_create_products, name="product-list-and-create"),
    path("<int:id>", views.read_update_and_delete_product_by_id,
         name="product-detail-update-and-delete"),
]
