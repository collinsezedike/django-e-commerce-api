from django.urls import path
from . import views

urlpatterns = [
    path(
        "",
        views.get_all_customer_profiles,
        name="customer-profile-list",
    ),
    path(
        "<int:id>",
        views.read_update_and_delete_customer_profile_by_id,
        name="customer-profile-detail-update-and-delete",
    ),
]

# There is no endpoint for creating a new customer profile
# because a new customer profile is created automatically 
# after a new customer user is created.
