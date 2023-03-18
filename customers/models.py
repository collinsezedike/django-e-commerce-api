from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import User


# Create your models here.
class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=1000)
    date_of_birth = models.DateField(null=True)
    phone_number = models.CharField(max_length=15)
    # profile_img

    def __str__(self):
        return self.user.first_name


@receiver(post_save, sender=User)
def create_customer_profile(sender, instance, created, **kwargs):
    """
    Create a blank customer profile when a new customer user is created.
    """
    if created and instance.type == "customer":
        new_customer_profile = CustomerProfile.objects.create(
            user=instance,
            address="",
            phone_number="",
        )
        new_customer_profile.save()
